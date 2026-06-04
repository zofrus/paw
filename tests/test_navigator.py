"""Tests for tutorial_engine navigation and content integrity."""

import curses
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tutorial_engine.content import (  # noqa: E402
    ALL_TRACKS,
    DISTINCTION_ART,
    PAGES,
    SECTIONS,
    TRACKS,
)
from tutorial_engine.engine import (  # noqa: E402
    Navigator,
    center_x,
    display_width,
    truncate_to_width,
)


# ── Navigator ─────────────────────────────────────────


def test_navigator_initial_state():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    assert nav.page == 0
    assert nav.current_section() == "Welcome"


def test_navigator_forward():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    action = nav.handle_key(curses.KEY_RIGHT)
    assert action == "next"
    assert nav.page == 1


def test_navigator_backward():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    nav.page = 5
    action = nav.handle_key(curses.KEY_LEFT)
    assert action == "prev"
    assert nav.page == 4


def test_navigator_no_underflow():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    nav.handle_key(curses.KEY_LEFT)
    assert nav.page == 0


def test_navigator_end_on_last_page():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    nav.page = len(PAGES) - 1
    action = nav.handle_key(curses.KEY_RIGHT)
    assert action == "end"
    assert nav.page == len(PAGES) - 1


def test_navigator_skip_section():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    nav.page = 0  # Welcome
    nav.handle_key(ord("s"))
    assert nav.current_section() == "The Problem"


def test_navigator_skip_from_last_section():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    nav.page = len(PAGES) - 1  # What's Next
    action = nav.handle_key(ord("s"))
    assert action == "end"


def test_navigator_quit():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    action = nav.handle_key(ord("q"))
    assert action == "quit"


def test_navigator_space_advances():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    action = nav.handle_key(ord(" "))
    assert action == "next"


def test_navigator_enter_advances():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    action = nav.handle_key(10)
    assert action == "next"


def test_navigator_n_advances():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    action = nav.handle_key(ord("n"))
    assert action == "next"


def test_navigator_full_traversal():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    for _ in range(len(PAGES) - 1):
        nav.handle_key(curses.KEY_RIGHT)
    assert nav.page == len(PAGES) - 1
    for _ in range(len(PAGES) - 1):
        nav.handle_key(curses.KEY_LEFT)
    assert nav.page == 0


def test_navigator_skip_all_sections():
    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    visited = [nav.current_section()]
    for _ in range(len(SECTIONS)):
        result = nav.handle_key(ord("s"))
        if result == "end":
            break
        visited.append(nav.current_section())
    assert visited == SECTIONS


# ── Content integrity ─────────────────────────────────


def test_page_count():
    assert len(PAGES) == 10


def test_section_count():
    assert len(SECTIONS) == 5


def test_all_pages_have_required_keys():
    for i, p in enumerate(PAGES):
        assert "title" in p, f"Page {i} missing title"
        assert "section" in p, f"Page {i} missing section"
        assert "body" in p, f"Page {i} missing body"


def test_all_page_sections_exist_in_sections():
    for i, p in enumerate(PAGES):
        sec = p["section"]
        assert sec in SECTIONS, f"Page {i} section '{sec}' not in SECTIONS"


def test_sections_appear_in_order():
    seen = []
    for p in PAGES:
        if p["section"] not in seen:
            seen.append(p["section"])
    assert seen == SECTIONS


def test_no_stale_12_references():
    import inspect

    from tutorial_engine import content

    src = inspect.getsource(content)
    assert "12 roles" not in src
    assert "12 specialized" not in src
    assert "11 of 12" not in src


def test_body_lines_fit_content_area():
    for i, p in enumerate(PAGES):
        for j, line in enumerate(p.get("body", [])):
            assert len(line) <= 60, (
                f"Page {i} ({p['title']}) body line {j} is {len(line)} chars"
            )


def test_art_fits_content_area():
    for i, p in enumerate(PAGES):
        for j, line in enumerate(p.get("art", [])):
            assert len(line) <= 60, (
                f"Page {i} ({p['title']}) art line {j} is {len(line)} chars"
            )


def test_distinction_art_row_colors_match():
    page = [p for p in PAGES if p["title"] == "The Key Distinction"][0]
    colors = page.get("art_row_colors", [])
    assert len(colors) == len(DISTINCTION_ART)


# ── Layout helpers ────────────────────────────────────


def test_center_x():
    assert center_x("hello", 80) == 37
    assert center_x("hi", 80) == 39
    assert center_x("a" * 100, 80) == 0


def test_display_width_ascii():
    assert display_width("hello") == 5


def test_display_width_wide_chars():
    assert display_width("日本") == 4


def test_truncate_to_width():
    assert truncate_to_width("hello world", 5) == "hello"
    assert truncate_to_width("日本語", 4) == "日本"
    assert truncate_to_width("abc", 10) == "abc"


# ── Multi-track tests ────────────────────────────────


def test_all_tracks_exist():
    assert len(TRACKS) == 5
    track_ids = {t["id"] for t in TRACKS}
    assert track_ids == {"learn", "start", "cli", "advanced", "practice"}


def test_all_tracks_have_content():
    for track in TRACKS:
        tid = track["id"]
        assert tid in ALL_TRACKS, f"Track {tid} missing from ALL_TRACKS"
        sections, pages = ALL_TRACKS[tid]
        assert len(pages) > 0, f"Track {tid} has no pages"
        assert len(sections) > 0, f"Track {tid} has no sections"


def test_all_track_pages_reference_valid_sections():
    for tid, (sections, pages) in ALL_TRACKS.items():
        for i, p in enumerate(pages):
            sec = p["section"]
            assert sec in sections, (
                f"Track {tid} page {i} section '{sec}' not in sections"
            )


def test_all_track_body_lines_fit():
    for tid, (_, pages) in ALL_TRACKS.items():
        for i, p in enumerate(pages):
            for j, line in enumerate(p.get("body", [])):
                assert len(line) <= 60, (
                    f"Track {tid} page {i} line {j}: {len(line)} chars"
                )


def test_all_track_art_fits():
    for tid, (_, pages) in ALL_TRACKS.items():
        for i, p in enumerate(pages):
            for j, line in enumerate(p.get("art", [])):
                assert len(line) <= 60, (
                    f"Track {tid} page {i} art {j}: {len(line)} chars"
                )


def test_all_track_navigation():
    for tid, (sections, pages) in ALL_TRACKS.items():
        nav = Navigator(len(pages), sections, pages)
        for _ in range(len(pages) - 1):
            nav.handle_key(curses.KEY_RIGHT)
        assert nav.page == len(pages) - 1, f"Track {tid} forward failed"
        for _ in range(len(pages) - 1):
            nav.handle_key(curses.KEY_LEFT)
        assert nav.page == 0, f"Track {tid} backward failed"
