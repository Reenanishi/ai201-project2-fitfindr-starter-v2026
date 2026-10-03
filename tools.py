"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""
import re
import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings

_STOPWORDS ={"a", "an", "and" , "the", "for", "with", "under","over", "in", "of"}

def _keywords(text: str) -> set[str]:
    """Lowercase words worth matching on, stopwords removed."""
    words = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {
        word for word in words
        if word not in _STOPWORDS and len(word) > 1
    }


def _size_tokens(size: str) -> set[str]:
    """Turn sizes such as S/M into separate size tokens."""
    cleaned = re.sub(r"\([^)]*\)", " ", size or "")

    parts = [
        part.strip().upper()
        for part in cleaned.split("/")
    ]

    return {part for part in parts if part}


def _size_matches(wanted: str, listing_size: str) -> bool:
    """Check whether the requested size matches the listing size."""
    if not wanted:
        return True

    listing_tokens = _size_tokens(listing_size)

    if any(
        token.startswith("ONE SIZE")
        for token in listing_tokens
    ):
        return True

    return bool(_size_tokens(wanted) & listing_tokens)





# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally
    a size and a maximum price.

    Args:
        description: Keywords describing what the user wants.
        size: A size to filter by, or None to skip the size filter.
        max_price: Maximum price, or None to skip the price filter.

    Returns:
        A list of matching listing dictionaries, best match first.
        Returns an empty list if nothing matches.
    """

    listings = load_listings()
    results = []

    wanted_words = _keywords(description)

    for listing in listings:

        # Filter by maximum price
        if max_price is not None and listing["price"] > max_price:
            continue

        # Filter by size
        if size is not None and not _size_matches(size, listing["size"]):
            continue

        # Combine searchable information from the listing
        searchable_text = " ".join([
            listing["title"],
            listing["description"],
            listing["category"],
            " ".join(listing["style_tags"]),
            " ".join(listing["colors"]),
        ])

        listing_words = _keywords(searchable_text)

        # Count how many search words match the listing
        score = len(wanted_words & listing_words)

        # Ignore listings with no matching words
        if score == 0:
            continue

        results.append((score, listing))

    # Put the best matches first
    results.sort(key=lambda item: item[0], reverse=True)

    # Return only the listing dictionaries
    return [
        listing
        for score, listing in results[:config.SEARCH_RESULT_LIMIT]
    ]

# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    """

    wardrobe_items = wardrobe.get("items", [])

    if not wardrobe_items:
        prompt = f"""
Give general styling advice for this thrifted item:

Item: {new_item['title']}
Description: {new_item['description']}
Colors: {', '.join(new_item['colors'])}
Style tags: {', '.join(new_item['style_tags'])}

Suggest one or two outfit ideas for this item.
"""
        return generate(prompt)

    wardrobe_text = "\n".join(
        f"- {item.get('name', 'Unnamed item')} "
        f"({item.get('category', 'unknown category')}, "
        f"colors: {', '.join(item.get('colors', []))})"
        for item in wardrobe_items
    )

    prompt = f"""
The user is considering this thrifted item:

Item: {new_item['title']}
Description: {new_item['description']}
Colors: {', '.join(new_item['colors'])}
Style tags: {', '.join(new_item['style_tags'])}

The user already owns these wardrobe items:

{wardrobe_text}

Suggest one or two outfits using the new item with specific pieces
from the user's wardrobe. Name the wardrobe pieces you recommend.
"""

    return generate(prompt)

# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    Args:
        outfit: The outfit suggestion from suggest_outfit().
        new_item: The listing dict for the thrifted item.

    Returns:
        A two-to-four sentence caption.
        If outfit is empty, returns a descriptive message.
    """

    # Handle an empty outfit
    if not outfit or not outfit.strip():
        return "No outfit suggestion was provided, so a fit card could not be created."

    prompt = f"""
Write a short 2-to-4 sentence social media caption about this thrifted find.

Item: {new_item['title']}
Price: ${new_item['price']:.2f}
Size: {new_item['size']}
Platform: {new_item['platform']}
Colors: {', '.join(new_item['colors'])}
Style tags: {', '.join(new_item['style_tags'])}

Outfit:
{outfit}

Make the caption sound like a real post rather than a product description.
Mention the item, price, size, and platform.
Be specific about the outfit's vibe.
"""

    return generate(prompt)