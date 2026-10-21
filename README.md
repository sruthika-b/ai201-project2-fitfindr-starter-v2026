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
```

---
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

FitFindr takes a clothing query, optionally including a size and maximum price, and searches thrift listings for relevant items. It selects the highest-ranked result and asks a model to suggest outfits using the user's wardrobe, or general styling advice if the wardrobe is empty. It then creates a short fit-card caption for the selected item and suggested outfit. If nothing matches, it stops and tells the user which parts of the query to change.

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

- **What it does:** Searches thrift listings for items matching the requested description, optionally filtered by size and maximum price. Compare lowercase alphanumeric query tokens after removing stopwords and one-character tokens against each listing's `description`; size matching is case-insensitive exact matching on slash-separated size tokens after removing parenthetical notes, with any `ONE SIZE` listing matching any requested size.
- **Inputs:** `description` (str), `size` (str | None), `max_price` (float | None).
- **Returns:** A list of matching listing dicts, each with `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`; include only listings at or below `max_price`, rank by descending keyword-overlap score, preserve dataset order for ties, and return no more than `config.SEARCH_RESULT_LIMIT` results.
- **When it has nothing:** Returns an empty list (`[]`) if no listing passes the filters and has at least one query-keyword match; `size=None` and `max_price=None` disable their respective filters.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits using the selected thrift item and the user's wardrobe.
- **Inputs:** `new_item` (listing dict), `wardrobe` (dict with an `items` list of wardrobe-item dicts containing `name`, `category`, `colors`, and `style_tags`, plus optional `notes`).
- **Returns:** A non-empty string with one or two outfit suggestions; when wardrobe items exist, each suggestion must name at least one piece from `wardrobe["items"]` and explain how it pairs with `new_item`.
- **When it has nothing:** If `wardrobe["items"]` is empty, return general styling advice for `new_item` without claiming the user owns any specific pieces; do not return an empty string or raise an error for an empty wardrobe.

### `create_fit_card`

- **What it does:** Writes a short, post-ready caption about the thrifted item and a suggested outfit.
- **Inputs:** `outfit` (str), `new_item` (dict).
- **Returns:** A two-to-four sentence caption based on `outfit` that names `new_item["title"]`, states its `price` and `platform` exactly once each, and describes the outfit's vibe.
- **When it has nothing:** If `outfit` is empty or whitespace, return a non-empty descriptive fallback naming the item's title, price, and platform, without inventing outfit details or raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, set `session["error"]` to a message suggesting the user change the item description, size, or maximum price, then return without calling `suggest_outfit` or `create_fit_card`. Otherwise, save the first result as `session["selected_item"]`, pass that item and the session wardrobe to `suggest_outfit`, then pass the saved item and outfit suggestion to `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regular expressions extract an optional size after `size` and an optional price after phrases such as `under`, `below`, `up to`, `maximum`, or `max`, or a `$` amount. The remaining text is used as the item description.

**What moves through the session:** `query` is parsed into `parsed` (`description`, `size`, `max_price`); `search_listings` results go into `search_results`; the first result is saved as `selected_item`; then `selected_item` and `wardrobe` produce `outfit_suggestion`, and `selected_item` plus `outfit_suggestion` produce `fit_card`. On an empty search, `error` is set and the later fields stay `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

```
Here are two wearable outfits featuring your new Vintage Levi's 501 Jeans:

### Outfit 1: Casual Streetwear
* **Thrifted Item:** Vintage Levi's 501 Jeans — Medium Wash (bottoms)
* **Top:** White ribbed tank top
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** 
The white ribbed tank top provides a clean, fitted base that balances the classic, straight-leg fit of the medium wash jeans. Adding the vintage black denim jacket leans into the denim-on-denim aesthetic while tying in the "vintage" and "streetwear" style tags. Finally, the chunky white sneakers and black crossbody bag keep the look casual, comfortable, andanchored in everyday streetwear.

### Outfit 2: Cozy Contrast
* **Thrifted Item:** Vintage Levi's 501 Jeans — Medium Wash (bottoms)
* **Top:** Oversized grey crewneck sweatshirt
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:**
This outfit plays with proportions by pairing the fitted, structured Levi's 501s with the oversized grey crewneck sweatshirt dropping below the hip. The black combat boots add a bit of edge that complements the streetwear vibe of the jeans, while the brown leather belt and black crossbody bag provide practical, stylish accessories to finish off the look.

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```
Nothing beats the effortless cool of these vintage Levi's 501 jeans in a classic medium wash. Grab them now for just $38.0 on depop to complete your favorite casual rotation. Pair them with crisp white sneakers for that timeless, off-duty weekend vibe.
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**
I wanted to take a stab in implementing the tracing as well which is a part of Unit 4, I took AIs help in understanding how tracing works and how I can incorporate them in checking the results at every steps.

- *What I asked for:* Can you help me with understanding the tracing library and how it can be used for verifying the results from every step.
- *What came back:* The tracing library is a run log, not an automatic correctness checker. It helps you see what the agent did, what each tool received, and what came back. You still compare those values with what you expected.

trace.start_trace() clears the previous run’s log.
trace.step(name, inputs=..., returned=..., note=...) prints a step and saves it for later. Call it after doing the step and saving its result in the session.
trace.get_trace() returns the recorded steps as text.
trace.check_iterations(count) is separate: it stops a loop that runs too many times. It doesn’t verify tool results.
- *What I changed:* This helped me understand the syntax and implement the tracing functionality

**Moment 2**

- *What I asked for:* Assume you are the best prompt critique, can you check my prompt for suggest outfit and list down the pros and cons of the prompt
- *What came back:* I reviewed the current suggest_outfit prompts in tools.py. The populated-wardrobe prompt gives the model the thrifted item and the user’s wardrobe, then asks for one or two wearable outfits using listed pieces. The empty-wardrobe prompt asks for general outfit ideas without assuming what the user owns.

Pros

It clearly describes the task and limits the response to one or two outfits.
Including wardrobe names, colors, categories, style tags, and notes gives the model useful context.
Asking it to use listed wardrobe pieces helps keep suggestions grounded and reduces invented ownership claims.
The empty-wardrobe branch handles a genuinely different case rather than sending an empty list as if it were a normal wardrobe.
Cons

“Wearable” is subjective; the prompt doesn’t define what makes an outfit practical or coherent.
It doesn’t require a consistent response format, so results may vary in structure and be harder to compare.
It asks for explanations, but doesn’t say how brief they should be.
The entire wardrobe is passed in. That’s fine for the sample size, but could become noisy as a user’s wardrobe grows.
The system instruction says to use only the provided item details. That may be overly restrictive if you want general fashion knowledge, such as familiar color-pairing advice.
It doesn’t ask for a particular occasion, season, or level of formality, so the model has to choose those assumptions itself.
The strongest part is that the prompt grounds suggestions in the actual wardrobe. The main improvement opportunity is to decide how consistent and concise you want the outfit response to be.

- *What I changed:* The cons helped me be aware of the limitations of the current system and I felt like the "wearable" part actually made sense, therefore, I have changed the prompt accordingly.

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
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item ID reaches `suggest_outfit` unchanged | 5 of 5 | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED | NOT VERIFIED (IDs absent from saved trace) |
| 4. Fit card mentions item, price, and platform | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Unavailable size returns no listing and stops before `suggest_outfit` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 6. Impossible price ceiling excludes matching item | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 7. Invalid size falls back to One Size listings | 5 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |

`criteria.md` currently has seven criteria, so this table includes all seven.
This log uses `results/run_2026-10-21_2146_before.md` for criteria 1–6 and
`results/run_2026-10-21_2235_before.md` for criterion 7. The XXS scenario
passes all five tries. Criterion 3 remains unverified because traces show item
titles, not IDs. Criterion 4's five captions meet the sentence-count and
content checks. The outfit suggestion is regenerated each try, so the run does
not hold the exact same item-and-outfit input fixed as the criterion specifies.

**Real output from one try for each criterion**, from
`results/run_2026-10-21_2146_before.md` (`run_eval.py::main` calls
`run_eval.py::run_once`, which calls `agent.py::run_agent`):

Criterion 1 — matching query completes. Source: `results/run_2026-10-21_2146_before.md`; recorded by `run_eval.py::write_report` from `agent.py::run_agent`:
```
- stopped early: no
- selected_item: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
- search_results: 8
[4] suggest_outfit
     in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[5] create_fit_card
     in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
Fit card:
Channel serious early-aughts energy in this 2003 tour bootleg graphic tee. Grab it on Depop for just $24 to easily style an effortless grunge look or a casual streetwear fit. DM to claim!
```

Criterion 2 — impossible query stops early. Source: `results/run_2026-10-21_2146_before.md`; branch and message produced by `agent.py::run_agent` and `agent.py::_nothing_found_message`, recorded by `run_eval.py::write_report`:
```
- stopped early: yes — Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
- selected_item: (none)
- search_results: 0
[2] search_listings (via MCP)
     out: [] (empty)
[3] branch
     →    search returned []: stopping before suggest_outfit
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
```

Criterion 3 — state handoff. Source: `results/run_2026-10-21_2146_before.md`; selected item and tool input traced by `agent.py::run_agent` and recorded by `run_eval.py::write_report`. The actual saved trace does not include IDs, so this output alone cannot verify ID equality:
```
- selected_item: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
     in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
```

Criterion 4 — fit-card content. Source: `results/run_2026-10-21_2146_before.md`; caption returned by `tools.py::create_fit_card`, called by `agent.py::run_agent` and recorded by `run_eval.py::write_report`:
```
Fit card:
Channel total 2000s grunge vibes with this vintage-style graphic tee, perfect for effortless streetwear or dressed up with tailored trousers. It's up for grabs on Depop for just $24.0! Grab it now to instantly level up your rotation.
```

Criterion 5 — unavailable requested size. Source: `results/run_2026-10-21_2146_before.md`; search branch handled by `agent.py::run_agent` after `mcp_server.py::search_listings` calls `tools.py::search_listings`, recorded by `run_eval.py::write_report`:
```
- Query: `90s track jacket in size XXS`
- stopped early: yes — Nothing in the listings matched description '90s track jacket in', size XXS.
- selected_item: (none)
- search_results: 0
[2] search_listings (via MCP)
     out: [] (empty)
[3] branch
     →    search returned []: stopping before suggest_outfit
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one.
```

Criterion 6 — matching description, impossible price ceiling. Source: `results/run_2026-10-21_2146_before.md`; search branch handled by `agent.py::run_agent` after `mcp_server.py::search_listings` calls `tools.py::search_listings`, recorded by `run_eval.py::write_report`:
```
- Query: `90s track jacket under $1`
- stopped early: yes — Nothing in the listings matched description '90s track jacket', under $1.
- selected_item: (none)
- search_results: 0
[2] search_listings (via MCP)
     out: [] (empty)
[3] branch
     →    search returned []: stopping before suggest_outfit
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; raise the price ceiling above $1.
```

Criterion 7 — invalid-size One Size fallback. Source: `results/run_2026-10-21_2235_before.md`; `run_eval.py::write_report` records the results from `agent.py::run_agent` calling `mcp_server.py::search_listings` and `tools.py::search_listings`:
```
- Query: `chunky cardigan in size XR`
- stopped early: no
- selected_item: Knit Cardigan — Chunky Brown ($35.0, depop)
- search_results: 6
[2] search_listings (via MCP)
     in:  dict with keys: description, size, max_price
     out: 6 items: Knit Cardigan — Chunky Brown, Platform Sneakers — White Chunky Sole, Platform Mary Janes — Black Patent … +3 more
     →    6 match(es)
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
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All five saved tries completed without stopping early, selected a listing, and included a fit card. |
| 2 | Impossible query stops before `suggest_outfit` | 5 of 5 | MET (5/5) | All five saved tries had zero search results, an actionable message, and no outfit or fit-card call. |
| 3 | Selected item ID reaches `suggest_outfit` unchanged | 5 of 5 | MISSED (0/5 verified) | The saved traces show the selected item title reaching `suggest_outfit`, but omit IDs, so none of the five tries proves the required ID equality. This is an evidence gap, not proof the handoff is wrong. |
| 4 | Fit card has item, price, and platform in 2–4 sentences for the same item and outfit | 4 of 5 | MISSED (0/5 valid fixed-outfit trials; 5/5 captions meet content checks) | All five captions are 2–3 sentences and mention the graphic tee, $24, and Depop, but `suggest_outfit` generated a different outfit between tries. The saved run therefore did not test repeated generations with the same item and outfit. |
| 5 | Unavailable size returns no listing and stops before `suggest_outfit` | 5 of 5 | MET (5/5) | All five XXS tries had zero search results, returned a suggestion to change the size, and stopped before outfit generation. |
| 6 | Impossible price ceiling excludes a matching item | 5 of 5 | MET (5/5) | All five saved tries returned an empty search for the matching jacket description under $1 and stopped before `suggest_outfit`, with a message to raise the ceiling. |
| 7 | Invalid size falls back to One Size listings | 5 of 5 | MISSED (0/5) | All five `XR` tries returned six search results and proceeded to outfit generation instead of restricting results to One Size listings. |

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
