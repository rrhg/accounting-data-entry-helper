import pyautogui
import time
from db import my_sqlalchemy, my_alembic
from db.cks_images import *

""" For intructions see file db.instructions:
"""
new_column6 = "column66"


def main():
    # my_sqlalchemy.save_value_in_db_client_column(
    #     client2, 'col_120', '120_value')

    # a = my_sqlalchemy._table_has_column('client', 'name')
    # print(a, f"client table has column {}")

    # my_sqlalchemy.create_client('vida')
    # time.sleep(10)
    # my_sqlalchemy.print_all_clients()

    delete_all_cks_images_for_period('2022-05')
    print_all_cks_images_for_this_client()

    # l = my_sqlalchemy.get_cks_imgs_numbers_for_period("2022-05")
    # print(l.sort())
    # print(sorted(l))

    # ck_number = "non" #"3538" # 3536, 3533
    ck_number = "3538" # 3536, 3533
    # img = my_sqlalchemy.get_ck_image_by_ck_number(ck_number)
    # ok = my_sqlalchemy.show_ck_image_if_ck_number(ck_number)
    # r = my_alembic.add_column_to_client_table("column66")
    
    # my_sqlalchemy.create_ck_image('a\path', '2022-05', 'vida')

    # cks_list = create_list_of_cks_objects()
    # for ck in cks_list:
    #     print(ck.img_path)
    #     print(ck.payee)

    # print_all_window_titles()
    # close_photos_window()

def close_photos_window():
    l = [w for w in pyautogui.getAllWindows()]
    title = next(w.title for w in l if " " in w.title)
    # title = next(w.title for w in l if "Photos" in w.title)
    w = pyautogui.getWindowsWithTitle(title)[0]
    # w.close()
    print(dir(w))

def get_all_window_titles():
    return [w for w in pyautogui.getAllWindows()]
    # return [w.title for w in pyautogui.getAllWindows()]
    # w title.strip() it was not printing check (quickbooks online nlr)
    # return [w.title.strip() for w in pyautogui.getAllWindows()]

def print_all_window_titles():
    for t in get_all_window_titles():

        # on some windows like Check - Google Chrome
        # only works if we print t.title
        # in the script, not here
        # maybe quickbooks is doing something
        print(t.title)


def create_list_of_cks_objects():
    class Ck:
        def __init__(self, img_path, payee):
            self.img_path = img_path
            self.payee = payee

    cks_list = []
    for i in range(1,5):
        ck = Ck("path/to/file", f"payee_{str(i)}")
        cks_list.append(ck)


# def tests_w_pickle():
#     # add_blob_column('ck_blob')
#     pickle_string = pickle.dumps(cks_list)
#     # print(pickle_string)
#     insert_to_1_column('vida', 'ck_blob', pickle_string)
#     pickle_string = get_row('vida')['cks_images']
#     cks_list = pickle.loads(pickle_string)

if __name__ == '__main__':
    main()
