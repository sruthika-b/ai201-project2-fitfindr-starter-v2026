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
from utils.stopwords import STOPWORDS as _STOPWORDS

def _keywords(text: str) -> set[str]:
    # Lowercase words worth matching on and stopwords removed.
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in set(words) if w not in _STOPWORDS and len(w) > 1}

def _size_tokens(size: str) -> set[str]:
    cleaned = re.sub(r"\([^)]*\)", " ", size or "")
    parts = [p.strip().upper for p in cleaned.split("/")]
    return {p for p in parts if p}

def _size_matches(wanted: str, listing_size: str) -> bool:
    if not wanted:
        return True
    listing_tokens = _size_tokens(listing_size)
    if any(token.startswith("ONE SIZE") for token in listing_tokens):
        return True
    return bool(_size_tokens(wanted) & listing_tokens)

# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # 1. Load every listing with load_listings().
    listings = load_listings()
    # 2. Filter by max_price and by size, when each is provided.
    if max_price is not None:
        listings = [l for l in listings if l["price"] <= max_price]
    if size is not None:
        listings = [l for l in listings if l["size"].upper() == size.upper()]
    # 3. Score what's left by keyword overlap with `description`.
    query_keywords = _keywords(description)
    scored_listings = [
        (len(query_keywords & _keywords(listing["description"])), listing)
        for listing in listings
    ]
    # 4. Drop anything scoring zero.
    scored_listings = [
        (score, listing) for score, listing in scored_listings if score > 0
    ]
    # 5. Sort by score, highest first, and return the listing dicts —
    #    at most config.SEARCH_RESULT_LIMIT of them.
    scored_listings.sort(key=lambda result: result[0], reverse=True)
    return [
        listing
        for score, listing in scored_listings[:config.SEARCH_RESULT_LIMIT]
    ]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    wardrobe_items = wardrobe.get("items", [])
    item_details = (
        f"Title: {new_item.get('title', 'Unknown item')}\n"
        f"Category: {new_item.get('category', 'unknown')}\n"
        f"Description: {new_item.get('description', '')}\n"
        f"Colors: {', '.join(new_item.get('colors') or [])}\n"
        f"Style tags: {', '.join(new_item.get('style_tags') or [])}"
    )

    if wardrobe_items:
        wardrobe_details = "\n".join(
            f"- {item.get('name', 'Unnamed item')} "
            f"(category: {item.get('category', 'unknown')}; "
            f"colors: {', '.join(item.get('colors') or [])}; "
            f"style tags: {', '.join(item.get('style_tags') or [])}; "
            f"notes: {item.get('notes') or 'none'})"
            for item in wardrobe_items
        )
        prompt = (
            f"Thrifted item:\n{item_details}\n\n"
            f"User's wardrobe:\n{wardrobe_details}\n\n"
            "Suggest one or two wearable outfits that include the thrifted item. "
            "Name pieces from the user's wardrobe exactly as listed, and do not "
            "claim they own anything that is not listed. Briefly explain why "
            "the pieces work together."
        )
        system = "You are a practical personal stylist. Use only the provided item details."
    else:
        prompt = (
            f"Thrifted item:\n{item_details}\n\n"
            "The user has not provided any wardrobe items. Give one or two "
            "general outfit ideas for styling this item, describing types of "
            "pieces or colors they could pair with it. Do not imply that the "
            "user already owns any specific pieces."
        )
        system = "You are a practical personal stylist. Give useful advice without assuming what the user owns."

    return generate(prompt, system=system)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    title = new_item.get("title", "This thrifted find")
    price = new_item.get("price", "price not listed")
    platform = new_item.get("platform", "platform not listed")

    if not outfit.strip():
        return (
            f"{title} is listed for ${price} on {platform}. "
            "Add an outfit suggestion to create a complete fit card."
        )

    prompt = (
        f"Thrifted item: {title}\n"
        f"Price: ${price}\n"
        f"Platform: {platform}\n"
        f"Outfit suggestion: {outfit}\n\n"
        "Write a natural, post-ready caption in 2 to 4 sentences. Mention the "
        "item, its price, and its platform exactly once each. Describe the "
        "outfit's vibe, and do not invent item details."
    )
    system = "Write concise, specific social captions with a natural voice."
    return generate(prompt, system=system)
