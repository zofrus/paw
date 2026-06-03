"""
paw tutorial TUI engine.
Single-file rendering, navigation, and effects. Python stdlib only (curses).
"""
import curses
import signal
import time

from tutorial_engine.content import PAGES, SECTIONS

# ── Color pairs ────────────────────────────────────────

CYAN = 1
GREEN = 2
YELLOW = 3
MAGENTA = 4
BOLD_WHITE = 5


def init_colors():
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(MAGENTA, curses.COLOR_MAGENTA, -1)
        curses.init_pair(BOLD_WHITE, curses.COLOR_WHITE, -1)
    except curses.error:
        pass


# ── Safe drawing helpers ───────────────────────────────

def safe_addstr(win, y, x, text, attr=0):
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x < 0:
        return
    available = w - x - 1
    if available <= 0:
        return
    try:
        win.addstr(y, x, text[:available], attr)
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


# ── Box drawing ────────────────────────────────────────

def draw_box(win, y, x, h, w, color=0):
    attr = curses.color_pair(color) if color else 0
    for col in range(x + 1, x + w - 1):
        safe_addch(win, y, col, curses.ACS_HLINE, attr)
        safe_addch(win, y + h - 1, col, curses.ACS_HLINE, attr)
    for row in range(y + 1, y + h - 1):
        safe_addch(win, row, x, curses.ACS_VLINE, attr)
        safe_addch(win, row, x + w - 1, curses.ACS_VLINE, attr)
    safe_addch(win, y, x, curses.ACS_ULCORNER, attr)
    safe_addch(win, y, x + w - 1, curses.ACS_URCORNER, attr)
    safe_addch(win, y + h - 1, x, curses.ACS_LLCORNER, attr)
    safe_addch(win, y + h - 1, x + w - 1, curses.ACS_LRCORNER, attr)


# ── Progress bar ───────────────────────────────────────

def draw_progress(win, y, x, width, current, total, color=CYAN):
    if total <= 0 or width < 10:
        return
    bar_width = width - 8
    filled = int(bar_width * (current + 1) / total)
    empty = bar_width - filled
    label = f"{current + 1}/{total}"
    bar = "[" + "=" * filled + "-" * empty + "]"
    safe_addstr(win, y, x, bar, curses.color_pair(color))
    safe_addstr(win, y, x + len(bar) + 1, label, curses.color_pair(color) | curses.A_DIM)


# ── Effects ────────────────────────────────────────────

def typewriter(win, y, x, text, attr=0, delay_ms=25):
    """Character-by-character text reveal. Any keypress completes instantly."""
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


def slide_in_lines(win, y, x, lines, attr=0, delay_ms=40):
    """Reveal lines one at a time top-to-bottom. Any keypress completes."""
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


# ── Navigation ─────────────────────────────────────────

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
        section_idx = self.sections.index(current_section)
        if section_idx < len(self.sections) - 1:
            next_section = self.sections[section_idx + 1]
            self.page = self.section_starts[next_section]
            return "next"
        return "end"

    def current_section(self):
        return self.pages[self.page]["section"]

    def section_index(self):
        return self.sections.index(self.current_section())


# ── Page Renderer ──────────────────────────────────────

def render_page(win, page, rows, cols, animate=False):
    """Render a single page. Returns early if animation was interrupted."""
    win.erase()

    content_width = min(cols - 4, 72)
    left_margin = max(1, (cols - content_width) // 2)

    title = page["title"]
    art = page.get("art")
    art_color = page.get("art_color", 0)
    body = page.get("body", [])
    highlight = page.get("highlight", {})
    do_typewriter = page.get("typewriter_title", False) and animate

    cur_y = 1

    # ── Title ──
    title_x = center_x(title, cols)
    title_attr = curses.color_pair(CYAN) | curses.A_BOLD

    if do_typewriter:
        interrupted = typewriter(win, cur_y, title_x, title, title_attr, delay_ms=40)
        if interrupted:
            animate = False
    else:
        safe_addstr(win, cur_y, title_x, title, title_attr)

    cur_y += 1

    # ── Title underline ──
    underline = "─" * len(title)
    safe_addstr(win, cur_y, title_x, underline, curses.color_pair(CYAN))
    cur_y += 1

    # ── Art ──
    if art:
        cur_y += 1
        art_attr = curses.color_pair(art_color) if art_color else 0

        if animate:
            interrupted = slide_in_lines(
                win, cur_y, left_margin, art, art_attr, delay_ms=30
            )
            if interrupted:
                animate = False
        else:
            for i, line in enumerate(art):
                safe_addstr(win, cur_y + i, left_margin, line, art_attr)
        cur_y += len(art)

    # ── Body ──
    cur_y += 1
    body_attr = curses.A_NORMAL

    if animate:
        interrupted = False
        for i, line in enumerate(body):
            line_attr = body_attr
            for prefix, color in highlight.items():
                stripped = line.lstrip()
                if stripped.startswith(prefix):
                    line_attr = curses.color_pair(color) | curses.A_BOLD
                    break
            safe_addstr(win, cur_y + i, left_margin, line, line_attr)
            win.refresh()
            curses.napms(25)
            win.nodelay(True)
            ch = win.getch()
            win.nodelay(False)
            if ch != -1:
                for j in range(i + 1, len(body)):
                    battr = body_attr
                    for pfx, col in highlight.items():
                        if body[j].lstrip().startswith(pfx):
                            battr = curses.color_pair(col) | curses.A_BOLD
                            break
                    safe_addstr(win, cur_y + j, left_margin, body[j], battr)
                break
    else:
        for i, line in enumerate(body):
            line_attr = body_attr
            for prefix, color in highlight.items():
                stripped = line.lstrip()
                if stripped.startswith(prefix):
                    line_attr = curses.color_pair(color) | curses.A_BOLD
                    break
            safe_addstr(win, cur_y + i, left_margin, line, line_attr)

    win.refresh()


def render_footer(win, nav, rows, cols):
    """Draw navigation hints, section name, and progress bar at the bottom."""
    footer_y = rows - 2

    section_name = nav.current_section()
    sec_attr = curses.color_pair(MAGENTA) | curses.A_BOLD
    safe_addstr(win, footer_y - 1, 2, f"  {section_name}", sec_attr)

    draw_progress(win, footer_y - 1, cols - 26, 24, nav.page, nav.total)

    hints = " [</>] Navigate   [s] Skip section   [q] Quit "
    hint_x = center_x(hints, cols)
    safe_addstr(win, footer_y, hint_x, hints, curses.color_pair(BOLD_WHITE) | curses.A_DIM)

    # thin line above footer
    for x in range(1, cols - 1):
        safe_addch(win, footer_y - 2, x, curses.ACS_HLINE, curses.color_pair(CYAN))

    win.refresh()


def render_too_small(win, rows, cols):
    """Show a friendly 'resize your terminal' message."""
    win.erase()
    msg1 = "Terminal too small"
    msg2 = f"Current: {cols}x{rows}"
    msg3 = "Need: 80x24 minimum"
    msg4 = "Please resize your terminal."

    cy = rows // 2 - 2
    for i, msg in enumerate([msg1, msg2, msg3, "", msg4]):
        if msg:
            safe_addstr(win, cy + i, center_x(msg, cols), msg,
                        curses.color_pair(YELLOW) | curses.A_BOLD)
    win.refresh()


# ── Main loop ──────────────────────────────────────────

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

        if rows < 24 or cols < 80:
            render_too_small(stdscr, rows, cols)
            key = stdscr.getch()
            if key == ord("q"):
                break
            continue

        page_changed = nav.page != last_page
        if page_changed:
            animate = nav.page not in visited
            visited.add(nav.page)
            render_page(stdscr, PAGES[nav.page], rows, cols, animate=animate)
            render_footer(stdscr, nav, rows, cols)
            last_page = nav.page

        key = stdscr.getch()
        if key == -1:
            continue

        action = nav.handle_key(key)
        if action == "quit":
            break
        elif action == "end":
            break


def main():
    curses.wrapper(run)
