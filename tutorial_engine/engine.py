"""
paw tutorial TUI engine.
Sidebar navigation, bordered layout, animations. Python stdlib only (curses).
"""

import curses
import signal

from tutorial_engine.content import PAGES, SECTIONS

# ── Color pairs ────────────────────────────────────────

CYAN = 1
GREEN = 2
YELLOW = 3
MAGENTA = 4
BOLD_WHITE = 5
SIDEBAR_HL = 6
BORDER = 7


def init_colors():
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(MAGENTA, curses.COLOR_MAGENTA, -1)
        curses.init_pair(BOLD_WHITE, curses.COLOR_WHITE, -1)
        curses.init_pair(SIDEBAR_HL, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(BORDER, curses.COLOR_CYAN, -1)
    except curses.error:
        pass


# ── Safe drawing ──────────────────────────────────────


def display_width(text):
    """Calculate terminal display width accounting for wide characters."""
    import unicodedata

    w = 0
    for ch in text:
        eaw = unicodedata.east_asian_width(ch)
        w += 2 if eaw in ("W", "F") else 1
    return w


def truncate_to_width(text, max_width):
    """Truncate text to fit within max_width terminal columns."""
    import unicodedata

    w = 0
    for i, ch in enumerate(text):
        eaw = unicodedata.east_asian_width(ch)
        cw = 2 if eaw in ("W", "F") else 1
        if w + cw > max_width:
            return text[:i]
        w += cw
    return text


def safe_addstr(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x < 0:
        return
    available = w - x - 1
    if available <= 0:
        return
    try:
        win.addstr(y, x, truncate_to_width(text, available), attr)
    except curses.error:
        pass


def safe_addch(win, y, x, ch, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w:
        return
    try:
        win.addch(y, x, ch, attr)
    except curses.error:
        pass


def center_x(text, width):
    return max(0, (width - len(text)) // 2)


def hline(win, y, x1, x2, attr=0):
    for x in range(x1, x2):
        safe_addch(win, y, x, curses.ACS_HLINE, attr)


def vline(win, x, y1, y2, attr=0):
    for y in range(y1, y2):
        safe_addch(win, y, x, curses.ACS_VLINE, attr)


# ── Layout constants ──────────────────────────────────

SIDEBAR_W = 20
MIN_COLS = 80
MIN_ROWS = 24


# ── Border + Frame ────────────────────────────────────


def draw_frame(win, rows, cols):
    ba = curses.color_pair(BORDER)

    # outer border
    safe_addch(win, 0, 0, curses.ACS_ULCORNER, ba)
    safe_addch(win, 0, cols - 1, curses.ACS_URCORNER, ba)
    safe_addch(win, rows - 1, 0, curses.ACS_LLCORNER, ba)
    safe_addch(win, rows - 1, cols - 1, curses.ACS_LRCORNER, ba)
    hline(win, 0, 1, cols - 1, ba)
    hline(win, rows - 1, 1, cols - 1, ba)
    vline(win, 0, 1, rows - 1, ba)
    vline(win, cols - 1, 1, rows - 1, ba)

    # title in top border
    title = " paw tutorial "
    tx = 3
    safe_addstr(win, 0, tx, title, curses.color_pair(CYAN) | curses.A_BOLD)

    # sidebar divider
    sx = SIDEBAR_W + 1
    safe_addch(win, 0, sx, curses.ACS_TTEE, ba)
    safe_addch(win, rows - 3, sx, curses.ACS_BTEE, ba)
    vline(win, sx, 1, rows - 3, ba)

    # footer separator
    hline(win, rows - 3, 1, cols - 1, ba)
    safe_addch(win, rows - 3, 0, curses.ACS_LTEE, ba)
    safe_addch(win, rows - 3, cols - 1, curses.ACS_RTEE, ba)


# ── Sidebar ───────────────────────────────────────────


def draw_sidebar(win, nav, rows):
    sx = 2
    sy = 2
    ba = curses.color_pair(BORDER)

    label = "SECTIONS"
    safe_addstr(win, sy, sx, label, curses.color_pair(CYAN) | curses.A_BOLD)
    sy += 1
    for x in range(sx, sx + SIDEBAR_W - 3):
        safe_addch(win, sy, x, curses.ACS_HLINE, ba)
    sy += 1

    current_sec = nav.current_section()

    for i, sec in enumerate(nav.sections):
        if sy + i >= rows - 4:
            break

        is_current = sec == current_sec
        sec_start = nav.section_starts.get(sec, 0)
        is_done = nav.page > sec_start and not is_current

        if is_current:
            marker = "▸"
            attr = curses.color_pair(SIDEBAR_HL) | curses.A_BOLD
            line = f" {marker} {sec:<{SIDEBAR_W - 5}}"
            safe_addstr(win, sy + i, sx, line, attr)
        elif is_done:
            marker = "✓"
            attr = curses.color_pair(GREEN)
            safe_addstr(win, sy + i, sx, f" {marker} {sec}", attr)
        else:
            marker = "·"
            attr = curses.A_NORMAL
            safe_addstr(win, sy + i, sx, f" {marker} {sec}", attr)

    # page counter at bottom of sidebar
    counter_y = rows - 4
    counter = f"{nav.page + 1}/{nav.total}"
    safe_addstr(win, counter_y, sx + 1, counter, curses.color_pair(CYAN))


# ── Effects ───────────────────────────────────────────


def typewriter(win, y, x, text, attr=0, delay_ms=25):
    for i in range(len(text)):
        safe_addstr(win, y, x, text[: i + 1], attr)
        win.refresh()
        curses.napms(delay_ms)
        win.nodelay(True)
        ch = win.getch()
        win.nodelay(False)
        if ch != -1:
            safe_addstr(win, y, x, text, attr)
            win.refresh()
            return True
    return False


def slide_in_lines(win, y, x, lines, attr=0, delay_ms=35):
    for i, line in enumerate(lines):
        safe_addstr(win, y + i, x, line, attr)
        win.refresh()
        curses.napms(delay_ms)
        win.nodelay(True)
        ch = win.getch()
        win.nodelay(False)
        if ch != -1:
            for j in range(i + 1, len(lines)):
                safe_addstr(win, y + j, x, lines[j], attr)
            win.refresh()
            return True
    return False


def cascade_lines(win, y, x, lines, attr=0, delay_ms=20):
    """Reveal body lines with a fast cascade. Feels snappy."""
    for i, line in enumerate(lines):
        safe_addstr(win, y + i, x, line, attr)
    win.refresh()
    return False


# ── Navigation ────────────────────────────────────────


class Navigator:
    def __init__(self, total_pages, sections, pages):
        self.page = 0
        self.total = total_pages
        self.sections = sections
        self.pages = pages
        self._build_section_map()

    def _build_section_map(self):
        self.section_starts = {}
        for i, page in enumerate(self.pages):
            sec = page["section"]
            if sec not in self.section_starts:
                self.section_starts[sec] = i

    def handle_key(self, key):
        if key in (curses.KEY_RIGHT, curses.KEY_DOWN, ord("n"), ord(" "), 10):
            if self.page < self.total - 1:
                self.page += 1
                return "next"
            return "end"
        elif key in (curses.KEY_LEFT, curses.KEY_UP, ord("p")):
            if self.page > 0:
                self.page -= 1
                return "prev"
        elif key == ord("s"):
            return self._skip_section()
        elif key == ord("q"):
            return "quit"
        return "none"

    def _skip_section(self):
        current_section = self.pages[self.page]["section"]
        try:
            section_idx = self.sections.index(current_section)
        except ValueError:
            return "end"
        if section_idx < len(self.sections) - 1:
            next_section = self.sections[section_idx + 1]
            self.page = self.section_starts[next_section]
            return "next"
        return "end"

    def current_section(self):
        return self.pages[self.page]["section"]

    def section_index(self):
        try:
            return self.sections.index(self.current_section())
        except ValueError:
            return 0


# ── Content Renderer ──────────────────────────────────


def render_content(win, page, rows, cols, animate=False):
    content_x = SIDEBAR_W + 3
    content_w = cols - content_x - 2
    content_y = 2

    title = page["title"]
    art = page.get("art")
    art_color = page.get("art_color", 0)
    body = page.get("body", [])
    highlight = page.get("highlight", {})
    do_typewriter = page.get("typewriter_title", False) and animate

    cur_y = content_y

    # title
    title_x = content_x + max(0, (content_w - len(title)) // 2)
    title_attr = curses.color_pair(CYAN) | curses.A_BOLD

    if do_typewriter:
        if typewriter(win, cur_y, title_x, title, title_attr, delay_ms=35):
            animate = False
    else:
        safe_addstr(win, cur_y, title_x, title, title_attr)

    cur_y += 1
    underline = "─" * min(len(title), content_w)
    ul_x = content_x + max(0, (content_w - len(underline)) // 2)
    safe_addstr(win, cur_y, ul_x, underline, curses.color_pair(CYAN))
    cur_y += 1

    # art
    if art:
        cur_y += 1
        art_attr = curses.color_pair(art_color) if art_color else 0
        row_colors = page.get("art_row_colors")

        if row_colors:
            for i, line in enumerate(art):
                rc = row_colors[i] if i < len(row_colors) else art_color
                attr = curses.color_pair(rc) if rc else art_attr
                safe_addstr(win, cur_y + i, content_x, line, attr)
            if animate:
                win.refresh()
                curses.napms(80)
        elif animate:
            if slide_in_lines(win, cur_y, content_x, art, art_attr, delay_ms=25):
                animate = False
        else:
            for i, line in enumerate(art):
                safe_addstr(win, cur_y + i, content_x, line, art_attr)
        cur_y += len(art)

    # body
    cur_y += 1
    for i, line in enumerate(body):
        if cur_y + i >= rows - 4:
            break
        line_attr = curses.A_NORMAL
        for prefix, color in highlight.items():
            if line.lstrip().startswith(prefix):
                line_attr = curses.color_pair(color) | curses.A_BOLD
                break
        safe_addstr(win, cur_y + i, content_x, line, line_attr)

    if animate and body:
        win.refresh()
        curses.napms(50)


# ── Footer ────────────────────────────────────────────


def render_footer(win, nav, rows, cols):
    fy = rows - 2
    hints = "[</>] Navigate  [s] Skip  [q] Quit"
    safe_addstr(win, fy, 3, hints, curses.color_pair(BOLD_WHITE))

    if nav.total == 0:
        return
    pct = int((nav.page + 1) / nav.total * 100)
    progress = f"{pct}%"
    safe_addstr(
        win,
        fy,
        cols - len(progress) - 3,
        progress,
        curses.color_pair(CYAN) | curses.A_BOLD,
    )


# ── Post-tutorial info screen ─────────────────────────


def render_finish_screen(win, rows, cols):
    win.erase()
    ba = curses.color_pair(BORDER)

    # border
    safe_addch(win, 0, 0, curses.ACS_ULCORNER, ba)
    safe_addch(win, 0, cols - 1, curses.ACS_URCORNER, ba)
    safe_addch(win, rows - 1, 0, curses.ACS_LLCORNER, ba)
    safe_addch(win, rows - 1, cols - 1, curses.ACS_LRCORNER, ba)
    hline(win, 0, 1, cols - 1, ba)
    hline(win, rows - 1, 1, cols - 1, ba)
    vline(win, 0, 1, rows - 1, ba)
    vline(win, cols - 1, 1, rows - 1, ba)

    title = " You're Ready "
    safe_addstr(win, 0, 3, title, curses.color_pair(GREEN) | curses.A_BOLD)

    cx = 4
    cy = 2

    lines = [
        ("WHAT TO DO RIGHT NOW", CYAN, True),
        ("", 0, False),
        ("If you ran ./setup, your hooks are already installed.", 0, False),
        ("Open Claude Code (or Cursor, or Codex CLI) and try:", 0, False),
        ("", 0, False),
        ("  1. Test the hooks:", BOLD_WHITE, False),
        ("     Type: git rebase main", YELLOW, False),
        ("     It will be blocked with an explanation.", 0, False),
        ("", 0, False),
        ("  2. Run a review agent:", BOLD_WHITE, False),
        ("     Type: Use the code-reviewer agent on", YELLOW, False),
        ("           the current diff.", YELLOW, False),
        ("", 0, False),
        ("  3. Stack multiple reviewers:", BOLD_WHITE, False),
        ("     Type: Use the code-reviewer, bug-auditor,", YELLOW, False),
        ("           and security-reviewer agents on", YELLOW, False),
        ("           the current diff.", YELLOW, False),
        ("", 0, False),
        ("WHERE TO LEARN MORE", CYAN, True),
        ("", 0, False),
        ("  Agents:   ~/.paw/agents/README.md", 0, False),
        ("  Hooks:    ~/.paw/hooks/README.md", 0, False),
        ("  Rules:    ~/.paw/rules/README.md", 0, False),
        ("  Full kit: github.com/zofrus/forge", 0, False),
    ]

    for i, (text, color, bold) in enumerate(lines):
        if cy + i >= rows - 2:
            break
        attr = curses.A_NORMAL
        if color:
            attr = curses.color_pair(color)
        if bold:
            attr |= curses.A_BOLD
        safe_addstr(win, cy + i, cx, text, attr)

    footer = "Press any key to exit"
    safe_addstr(
        win, rows - 2, center_x(footer, cols), footer, curses.color_pair(BOLD_WHITE)
    )

    win.refresh()
    win.timeout(-1)
    win.getch()


# ── Too-small screen ──────────────────────────────────


def render_too_small(win, rows, cols):
    win.erase()
    messages = [
        "Terminal too small",
        f"Current: {cols}x{rows}",
        f"Need: {MIN_COLS}x{MIN_ROWS} minimum",
        "",
        "Please resize your terminal.",
    ]
    cy = max(0, rows // 2 - 2)
    for i, msg in enumerate(messages):
        if msg:
            safe_addstr(
                win,
                cy + i,
                center_x(msg, cols),
                msg,
                curses.color_pair(YELLOW) | curses.A_BOLD,
            )
    win.refresh()


# ── Main loop ─────────────────────────────────────────


def run(stdscr):
    init_colors()
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    stdscr.timeout(100)

    nav = Navigator(len(PAGES), SECTIONS, PAGES)
    visited = set()
    resize_flag = [False]

    def handle_resize(signum, frame):
        resize_flag[0] = True

    signal.signal(signal.SIGWINCH, handle_resize)

    last_page = -1

    while True:
        rows, cols = stdscr.getmaxyx()

        if resize_flag[0]:
            resize_flag[0] = False
            curses.resizeterm(rows, cols)
            stdscr.clear()
            last_page = -1

        if rows < MIN_ROWS or cols < MIN_COLS:
            render_too_small(stdscr, rows, cols)
            key = stdscr.getch()
            if key == ord("q"):
                break
            continue

        page_changed = nav.page != last_page
        if page_changed:
            stdscr.erase()
            draw_frame(stdscr, rows, cols)
            draw_sidebar(stdscr, nav, rows)

            animate = nav.page not in visited
            visited.add(nav.page)
            render_content(stdscr, PAGES[nav.page], rows, cols, animate=animate)
            render_footer(stdscr, nav, rows, cols)
            stdscr.refresh()
            last_page = nav.page

        key = stdscr.getch()
        if key == -1:
            continue

        action = nav.handle_key(key)
        if action == "quit":
            break
        elif action == "end":
            render_finish_screen(stdscr, rows, cols)
            break


def main():
    curses.wrapper(run)
