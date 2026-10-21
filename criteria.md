# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
I chose 4 of 5 instead of 5 of 5 because the search uses keyword matching, so some query phrasings may fail to find a relevant listing. The outfit and fit-card tools also depend on model calls, which can occasionally fail, 4 successful end-to-end runs still sets a high bar without assuming every run will succeed.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
We shouldn't ideally make any further calls with 0 search search results, those are unwanted calls and adds no value to the user's query, we need to add an early exit before calling any further tools with no search results consistently.
---

## 3. Something about state

For matching queries, in 5 of 5 tries, the id of the item passed to suggest_outfit matches the id of session["selected_item"].

**Why this target:**
I picked 5 of 5 because passing the selected item between tools is a direct state handoff, so it should be consistent every time.

---

## 4. Something about the fit card

For five fit-card generations using the same item and outfit, at least four captions must be 2–4 sentences and mention the item, its price, and the platform. The wording can vary.

**Why this target:**
I chose 4 of 5 because the model can phrase the same caption differently and may occasionally leave out a detail. Requiring the key information in most outputs still sets a clear quality bar while allowing for that variation.

---

## 5. Unavailable size returns no listing

Given a query whose description matches a listing but requests size XXS, which is not present for that item in the catalog, `search_listings` returns an empty list and the agent stops before `suggest_outfit` in 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because an explicit size request is a hard filter: the agent should not suggest an item in a different size when no matching size is listed. The item description is known to match, so this specifically checks the size filter and empty-result branch.

## 6. An impossible price ceiling excludes a matching item

Given a query whose description matches a listing but whose maximum price is below that listing's price, `search_listings` returns an empty list and the agent stops before `suggest_outfit` in 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because the maximum price is an explicit numeric limit, so a result over budget is never acceptable. The query deliberately uses an item that exists in the catalog, which checks that the price filter—not an unrelated description mismatch—causes the empty result.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
