"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. That branch is the graded part of this unit.

Build and test your three tools in tools.py first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable
from mcp_client import call_tool


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    Every tool result is stored in the session, and the next step reads
    the value back out of the session.
    """
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# ── parsing the query ─────────────────────────────────────────────────────────

_SIZE_WORDS = r"XXS|XS|S|M|L|XL|XXL"

_PRICE_RE = re.compile(
    r"(?:under|below|less than|max|up to)?\s*\$\s*(\d+(?:\.\d+)?)",
    re.I,
)

_SIZE_RE = re.compile(
    rf"\bsize\s+({_SIZE_WORDS}|US\s*\d+(?:\.\d+)?|W\d+)\b",
    re.I,
)

_BARE_SIZE_RE = re.compile(
    rf",\s*({_SIZE_WORDS})\s*$",
    re.I,
)


def parse_query(query: str) -> dict:
    """
    Pull description, size, and max_price from the user's query.
    """
    text = query or ""

    # Find and remove the price.
    max_price = None
    price_match = _PRICE_RE.search(text)

    if price_match:
        max_price = float(price_match.group(1))
        text = (
            text[:price_match.start()]
            + " "
            + text[price_match.end():]
        )

    # Find and remove the size.
    size = None
    size_match = _SIZE_RE.search(text) or _BARE_SIZE_RE.search(text)

    if size_match:
        size = re.sub(
            r"\s+",
            " ",
            size_match.group(1),
        ).strip().upper()

        text = (
            text[:size_match.start()]
            + " "
            + text[size_match.end():]
        )

    # Whatever is left becomes the search description.
    description = re.sub(r"[,\s]+", " ", text).strip(" ,")

    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the FitFindr planning loop once.

    Branch rule:
    If search_listings returns an empty list, stop before suggest_outfit
    and tell the user what they can change.

    Otherwise, select the first result and continue through
    suggest_outfit and create_fit_card.
    """

    # 1. Start the session.
    session = new_session(query, wardrobe)

    # 2. Parse the user's query and save it in the session.
    session["parsed"] = parse_query(session["query"])

    # 3. Read the parsed values back out of the session and search.
    session["search_results"] = call_tool("search_listings", {
        "description": session["parsed"]["description"],
        "size": session["parsed"]["size"],
        "max_price": session["parsed"]["max_price"],
    })
    # 4. THE BRANCH:
    # If search returned nothing, stop here.
    if not session["search_results"]:
        session["error"] = _nothing_found_message(
            session["parsed"]
        )
        return session

    # 5. Choose the first result and save it in the session.
    session["selected_item"] = session["search_results"][0]

    # 6. Read the selected item and wardrobe back from the session.
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"],
        session["wardrobe"],
    )

    # 7. Read the outfit and selected item back from the session.
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"],
        session["selected_item"],
    )

    # 8. Return the finished session.
    return session


# ── no-results message ────────────────────────────────────────────────────────

def _nothing_found_message(parsed: dict) -> str:
    """
    Give the user useful things they can change when nothing matches.
    """

    tried = [
        f"description {parsed['description']!r}"
    ]

    if parsed["size"]:
        tried.append(
            f"size {parsed['size']}"
        )

    if parsed["max_price"] is not None:
        tried.append(
            f"under ${parsed['max_price']:g}"
        )

    suggestions = [
        "try broader search words"
    ]

    if parsed["size"]:
        suggestions.append(
            "remove the size or try another size"
        )

    if parsed["max_price"] is not None:
        suggestions.append(
            f"raise the price limit above ${parsed['max_price']:g}"
        )

    return (
        "Nothing in the listings matched "
        + ", ".join(tried)
        + ". Things to change: "
        + "; ".join(suggestions)
        + "."
    )


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(
            f"  fit_card is {session['fit_card']!r} "
            "— it should still be None here"
        )
        return

    item = session["selected_item"] or {}

    print(
        f"  found:    {item.get('title')} — "
        f"${item.get('price')} on {item.get('platform')}"
    )

    print(
        f"  outfit:   {session['outfit_suggestion']}"
    )

    print(
        f"  fit card: {session['fit_card']}"
    )


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")

    _show(
        run_agent(
            query="looking for a vintage graphic tee under $30",
            wardrobe=get_example_wardrobe(),
        )
    )

    print("\n=== A query it can't ===")

    _show(
        run_agent(
            query="designer ballgown size XXS under $5",
            wardrobe=get_example_wardrobe(),
        )
    )

    print(
        "\nThe second one should stop before the fit card. "
        "If both paths look the same,\n"
        "the branch isn't doing anything yet."
    )