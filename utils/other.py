import sys, os
from rich.console import Console
import pyautogui

red = Console(style="red")

def get_config():
    import config
    return config

def ask_to_continue():
    a = red.input('\n Do you want to continue? (y/n) : ')
    while True:
        if a == 'y' or a == 'Y':
            break
        elif a == 'n' or a == 'N':
            sys.exit(1) 


def close_photos_windows_app():
    l = [w for w in pyautogui.getAllWindows()]
    title = next(w.title for w in l if "Photos" in w.title)
    w = pyautogui.getWindowsWithTitle(title)[0]
    w.close()

def activate_powershell():
    l = [w for w in pyautogui.getAllWindows()]
    title = next(w.title for w in l if "PowerShell" in w.title)
    w = pyautogui.getWindowsWithTitle(title)[0]
    w.activate()

