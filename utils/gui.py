import sys, os, time
from rich.console import Console
import pyautogui
import autoit
import pygetwindow as gw
from .other import ask_to_continue
import pywinauto
red = Console(style="red")


def get_all_window_titles():
    l = [w for w in pyautogui.getAllWindows()]
    return [w.title for w in l]

def print_titles():
    titles = get_all_window_titles()
    for t in titles:
        print(f"=>{t}<=")

def get_window_title_w_str(string):
    titles = get_all_window_titles()
    for t in titles:
        # print(f"\n title: {t}")
        # print(f" string: {string}\n")
        if string in t:
            return t
    return ""

def focus_to_window(window_title=None):
    """ For some reason, pyautogui & autoit can fail to activate when is a browser. In those case, we can use this"""
    print(f"\n Edge should be opened.   Now we r looking for a windows title with the string Edge, activate it, & open the satemenet pdf")
    ask_to_continue()
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
    while True:
        if window.isActive == True:
            break
        else:
            print(f"...waiting for Edge window to show active...")
            time.sleep(1)

    # window.minimize() # these 3 could also work (to focus)
    # window.maximize()
    # window.restore()
    # ==> these did not worked
    # w = pyautogui.getWindowsWithTitle(title)[0]
    # w.activate()
    # autoit.win_wait_active(title, 10)


def activate_edge_n_open_file(file_path):

    # title = get_window_title_w_str("Microsoft  Edge")
    title = get_window_title_w_str("Edge")
    if not title:
        print(f"\n Did not found window w title: {title} \n ")
    focus_to_window(title)
    pre = r"file:///"
    url = pre + file_path
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)
    # pyautogui.hotkey('ctrl', 'l')
    pyautogui.write(url)
    time.sleep(1)
    pyautogui.press('enter')


def close_photos_windows_app():
    l = [w for w in pyautogui.getAllWindows()]
    titles = [w.title for w in l]
    for t in titles:
        print(t)

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


def open_edge(file_path: str, str_in_window_title = '', wait=1):
    # file:///C:/Users/r/OneDrive%20-%20H&J%20Accounting/Hogar%20Sol%20de%20Vida/Accounting%20y%20Estados%20Bancarios%20HSDV/Estados%20Banco%20HSDVida/2022/2022-05%20BANK%20STATEMENT%20VIDA.pdf
    pre = r"file:///"
    url = pre + file_path
    # a = input('Make sure no Chrome IRS page is open!!. Continue ? ')
    # while True:
    #     if a == 'y' or a == 'Y': break
    #     if a == 'n' or a == 'N': raise Exception('Canceled by user')

    # old_titles = get_all_window_titles()
    # print('old_titles: ');print(old_titles); print()

    pid = autoit.run("msedge.exe --start-maximized " + url )
    # pid = autoit.run("chrome.exe --start-maximized " + url )
    # "C:\Users\Public\Desktop\Microsoft Edge.lnk"
    # C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --profile-directory="Profile 1" for my Work profile. "Default" is for my personal profile.

    # print(wait)
    time.sleep( wait )

    # titles = get_all_window_titles()
    # # print('titles: ');print(titles); print()

    # window_object = None
    # for nt in titles:
    #     if nt not in old_titles:
    #         window_object = nt
    # if not window_object:
    #     window_object = window_title_that_includes(str_in_window_title)
    #     if not window_object:        
    #         # print(" Did not find a new window title. Maybe 3 seconds were not enough to load page")
    #         raise Exception(f'Did not find a new window title. Maybe {str(wait)} seconds were not enough to load page & the str_in_window_title was not found in any title'+
    #                         ' '+
    #                         '' # may need to add some info here
    #                         )
    # title = window_object.title 
    # autoit.win_move(title , 0, 0) # monitor # 1
    # autoit.win_wait_active(title, 15)
    # autoit.win_set_state(title , flag=3 ) # 3 == flag='SW_MAXIMIZE'
    
    # time.sleep( round(uniform(1.3, 1.5), 2)   )
    return title    

def get_window_handel_by_pid():
    # https://stackoverflow.com/questions/37501191/how-to-get-windows-window-names-with-ctypes-in-python
    pass