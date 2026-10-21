"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Empty wardrobe and no matching listing; this diagnostic expects [] search results.
        "name": "empty wardrobe with no search matches",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Repeated by run_eval.py five times to inspect fit-card quality.
        "name": "fit card has item facts",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # The item description matches, but the catalog has no XXS track jacket.
        "name": "matching item unavailable in requested size",
        "query": "90s track jacket in size XXS",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # Description matches the catalog, but no item is this inexpensive.
        "name": "matching item above price ceiling",
        "query": "90s track jacket under $1",
        "wardrobe": "example",
        "criterion": 6,
    },
    {
        # Unsupported size should fall back only to One Size catalog items.
        "name": "invalid size falls back to One Size",
        "query": "chunky cardigan in size XR",
        "wardrobe": "example",
        "criterion": 7,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 6):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
