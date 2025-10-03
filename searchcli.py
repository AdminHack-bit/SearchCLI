#!/usr/bin/python3
import curses
import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib.parse
import subprocess

DEBUG = False  # ASCII mode if True
DUCKHTML = "https://duckduckgo.com/html/"
USE_LYNX = True  # Set True to open links in lynx (CLI only)

def extract_real_url(href):
    """
    DuckDuckGo HTML results often wrap URLs as /l/?kh=-1&uddg=<encoded_url>
    This extracts and decodes the real URL.
    """
    parsed = urllib.parse.urlparse(href)
    query = urllib.parse.parse_qs(parsed.query)
    if 'uddg' in query:
        return urllib.parse.unquote(query['uddg'][0])
    return href

def fetch_results(query):
    results = []
    resp = requests.get(DUCKHTML, params={"q": query}, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    for a in soup.find_all("a", class_="result__a"):
        href = a.get("href")
        title = a.get_text()
        if href and title:
            url = extract_real_url(href)
            results.append({"title": title, "url": url})

    return results

def run_tui(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr("╔══════════════════════╗\n")
    stdscr.addstr("║   SearchCLI v1.0.0   ║\n")
    stdscr.addstr("║      [________]      ║\n")
    stdscr.addstr("╚══════════════════════╝\n")
    stdscr.addstr("Press S then Enter to Search!\n")
    stdscr.refresh()

    keypress = stdscr.getkey()
    if keypress.lower() != 's':
        return

    stdscr.addstr("Search: ")
    curses.echo()
    search = stdscr.getstr().decode()
    curses.noecho()
    stdscr.clear()
    stdscr.addstr(f"Searching for: {search}\n")
    stdscr.refresh()

    results = fetch_results(search)

    if not results:
        stdscr.addstr("\nNo results found.\n")
        stdscr.getch()
        return

    idx = 0
    scroll = 0

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        visible = results[scroll:scroll + max_y - 1]

        for i, item in enumerate(visible):
            prefix = "=> " if i + scroll == idx else "   "
            text = f"{prefix}{item['title']} [URL] {item['url']}"
            if len(text) > max_x - 1:
                text = text[:max_x - 1]
            stdscr.addstr(text + "\n")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and idx > 0:
            idx -= 1
            if idx < scroll:
                scroll -= 1
        elif key == curses.KEY_DOWN and idx < len(results) - 1:
            idx += 1
            if idx >= scroll + max_y - 1:
                scroll += 1
        elif key in (10, 13):  # Enter
            url = results[idx]['url']
            if USE_LYNX:
                subprocess.run(["lynx", url])
            else:
                webbrowser.open(url)
        elif key in (27, ord('q')):  # ESC or q
            break

if __name__ == "__main__":
    if DEBUG:
        print("ASCII mode not implemented yet")
    else:
        curses.wrapper(run_tui)