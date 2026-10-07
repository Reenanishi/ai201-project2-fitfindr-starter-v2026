# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

The user tells FitFindr what kind of clothing item they are looking for, FitFindr search the available items listings to find a matching item. Once an item is found, it will suggest using the user's wardrobe. Finally, it will create a short fit card for the items with a description of the outfit.

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**  It searches the available listings and finds items that matche with what the user is looking for.

- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" --> `description` (str), `size` (str or None), `max_price` (float or None)

- **Returns:** A list of listing dictionaries, each with details like `title`, `price`, `size`, and `platform`, with the best matches first.

- **When it has nothing:** Returns an empty list `[]` when no listings match with the user's search.

### `suggest_outfit`

- **What it does:** It suggests an outfit using the item found from the search and items from the user's wardrobe.

- **Inputs:** `new_item` (dict), `wardrobe` (dict)

- **Returns:** A non-empty string with an outfit suggestion.

- **When it has nothing:** If the wardrobe is empty, it should return general styling advice for the new item.

### `create_fit_card`

- **What it does:** It creates a short caption for the outfit and the new item.

- **Inputs:** `outfit` (str), `new_item` (dict)

- **Returns:** A 2–4 sentence fit card that describes the outfit and the new item.

- **When it has nothing:** If the outfit is empty, it returns a message explaining that there is no outfit to create a fit card for.

---

## Planning Loop
**Branch rule:** If `search_listings` returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to `suggest_outfit`.
**Where it lives:** `agent.py::run_agent`

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->





**How the query is parsed:** `agent.py::parse_query` uses regular expressions to find the size and maximum price in the user's query. The remaining text is used as the item description.


**What moves through the session:** The parsed query goes into `session["parsed"]`, the search results go into `session["search_results"]`, the first matching item goes into `session["selected_item"]`, the outfit suggestion goes into `session["outfit_suggestion"]`, and the final fit card goes into `session["fit_card"]`.
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
**One full query**

```text
$ python app.py ask 'vintage graphic tee under $30'

Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two outfit ideas using the new Y2K butterfly baby tee and pieces from your existing wardrobe:

**Outfit 1: Casual Streetwear (Y2K Daily)**
* **Top:** Y2K Butterfly Baby Tee (New Item)
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Outerwear:** Black cropped zip hoodie (worn open or draped over the shoulders)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

*Why it works:* This leans into the Y2K aesthetic of the baby tee by balancing the fitted crop top with loose, low-slung baggy denim. The black hoodie and white sneakers tie the monochrome elements of the look together while letting the pink and purple butterfly graphic pop.

**Outfit 2: Elevated Casual (Soft & Edgy Contrast)**
* **Top:** Y2K Butterfly Baby Tee (New Item)
* **Bottoms:** Wide-leg khaki trousers
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt, Black crossbody bag

*Why it works:* Pairing the super-feminine, pastel butterfly tee with wide-leg utility trousers creates a cool high-low mix. Tucking the tee in with the brown leather belt defines the waist, and the black combat boots and vintage denim jacket add an effortless, slightly edgy contrast to the soft cottagecore/Y2K vibe.

Fit card: Fluttered into my closet and I am obsessed with this Y2K butterfly babytee! 🦋✨ Listed on my Depop in a size S/M for just $18, it’s giving the ultimate soft-meets-edgy contrast when paired with baggy denim and combat boots. Go grab it before I change my mind and keep it for myself!
```



**The three tools, tested one at a time**

```text
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit suggestions using the vintage Levi's 501s and pieces from your existing wardrobe:

### Outfit 1: Effortless Casual Streetwear
This look leans into the classic, laid-back vibe of the 501s with comfortable, everyday basics.
* Top: White ribbed tank top
* Outerwear: Oversized grey crewneck sweatshirt
* Shoes: Chunky white sneakers
* Accessories: Black crossbody bag

### Outfit 2: Edgy Denim-on-Denim
Pairing the medium wash jeans with black outerwear creates a high-contrast, vintage-inspired streetwear look.
* Top: Black cropped zip hoodie
* Outerwear: Vintage black denim jacket
* Shoes: Black combat boots
* Accessories: Brown leather belt and black crossbody bag
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Nothing beats the effortless streetwear vibe of a crisp white sneaker paired with the ultimate classic denim. These vintage medium wash Levi’s 501s have that perfectly broken-in look and are ready for a new home. Grab this W30 L30 staple for just $38 over on my Depop before they’re gone! #vintage #denim
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked AI for help building and testing `search_listings` so it would filter listings by description, size, and maximum price.

- *What came back:* AI helped me identify problems with the filtering logic and showed me how to test both a normal search and a search that should return no matches.
- *What I changed:* I fixed the filtering logic so matching listings are returned correctly and an impossible search returns an empty list `[]`.


**Moment 2**

- *What I asked for:* I asked AI why `create_fit_card` was giving me the same caption when I ran the test multiple times.

- *What came back:*AI suggested checking the temperature and cache settings. I checked `config.py` and found that the temperature was `0.9` but caching was enabled.

- *What I changed:* I tested the function again with `AI201_CACHE=0`. The captions changed between runs, which showed me that the repeated response was caused by the cache.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
