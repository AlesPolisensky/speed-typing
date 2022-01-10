import curses
from curses import wrapper
import time
import random

def start(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the speed typing test.")
    stdscr.addstr("\nPress any key to begin.")
    stdscr.refresh() 
    stdscr.getkey()

def disp_text(stdscr, text, current, wpm = 0):
    stdscr.addstr(text)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    
    for idx, char in enumerate(current):
        correct_character = text[idx]
        color = curses.color_pair(1)
        if char != correct_character:
            color = curses.color_pair(2)
        stdscr.addstr(0, idx, char, color)
def load_text():
    with open("lorem_ipsum.txt", "r",) as f:
        lines = f.readlines()
        return random.choice(lines).strip()
       
def typing_test(stdscr):
    text = load_text()
    current_text = []
    wpm = 0
    start_timer = time.time()
    stdscr.nodelay(True)
    while True:
        time_elapsed = max(time.time() - start_timer, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        
        stdscr.clear()
        disp_text(stdscr, text, current_text, wpm)
        stdscr.refresh()
        
        if "".join(current_text) == text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue
        
        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(text):    
            current_text.append(key)


        
def typing(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    start(stdscr)
    while True:
        typing_test(stdscr)
        
        stdscr.addstr(2,0, "You completed the text. Press any key to continue. Press ESC to exit.")
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break
    
wrapper(typing)
