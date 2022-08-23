from config import ENTERED_CHECKS_FILE, client, client_name, PATH_FOR_OUTPUT, PERIOD, CKS_PAYEES_IMAGES_DIR
from utils.entered_checks import (ck_was_already_entered, 
                                  get_already_entered_ck_info,
                                  add_to_entered_checks)
                                #   get_trans_from_vendor_dict)
from client_partner import (get_debit_transaction_from_check_line,
                            get_or_create_vendor_dict_from_ck_line)
from utils.other import ask_to_continue
from utils.gui import close_photos_windows_app, activate_powershell
# from db.cks_images import this_period_cks_images_done, show_ck_image_by_ck_number, save_payee_img_in_vendor_dir
from db.cks_images import *
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


def convert_checks_lines_into_transactions( checks_lines, transactions ):
    ck_nums_found = []
    previous_line = ''

    # if we got here, means client has checks & should get cks imgs & payees so we can use them in each transaction
    client_have_cks_imgs = get_cks_images_if_not_done_for_this_period()

    for ck_line in checks_lines:
        print_ck_line(ck_line) 
        ck_number = client.get_ck_number_from_ck_line( ck_line )
        need_to_close_photos_app = False

        # ignore duplicated cks
        if ( client.use_only_the_1st_ck_when_duplicated() and ck_number in ck_nums_found):
            red.print(f'\nIgnoring ck# {ck_number} because it was already added & the client function use_only_the_1st_ck_when_duplicated() is set to True \n')

        else:
            ck_nums_found.append(ck_number)
            vendor_dict = {}
            vendor_dict["memo"] = ""

            if hasattr(client, 'vendor_key_when_client_enters_checks_info'):
                vendor_dict['partner_key'] = client.vendor_key_when_client_enters_checks_info()
                # do search for vendor dict info. check info is just for reconciliation

            elif ck_was_already_entered( ck_number, ENTERED_CHECKS_FILE):
                vendor_dict = get_already_entered_ck_info( ck_number, ENTERED_CHECKS_FILE)
                # print(vendor_dict)
                # vendor_dict["partner_key"] = vendor_dict["vendor_key"]

            # New check ! Need to get data, so show ck image if we have it
            else:
                need_to_close_photos_app = show_ck_image(ck_number, client_have_cks_imgs)
                found_ck_image = need_to_close_photos_app
                vendor_dict = get_or_create_vendor_dict_from_ck_line(
                                             ck_line,
                                             ck_number,
                                             client_have_cks_imgs,
                                             found_ck_image,
                                             ask_n_show_all_cks_images )
                # now we know the vendor for new check, so save ck payee img under this vendor for future hugginface handwritten model tunning
                save_payee_img_in_vendor_dir( CKS_PAYEES_IMAGES_DIR, vendor_dict['name'],ck_number)
                add_to_entered_checks( vendor_dict, ENTERED_CHECKS_FILE )

            new_transactions = get_debit_transaction_from_check_line(
                                              vendor_dict,
                                              ck_line,
                                              previous_line,
                                              )

            # done getting all check data so we can close ck image
            if need_to_close_photos_app:
                close_photos_windows_app()
   
            for t in new_transactions:
                transactions.append( t )
                t.log_without_train(ck_line, previous_line)
                """ 
                    Not training model with checks lines (for now) bc it seems that check lines are not relevant to find the vendor. That's why we ask the user to enter the vendor for each check. Check line only have ck number, date, & those do not tell us anything about the vendor
                    trans.log_and_train( ck_line, "" ) # previous line in cks is not relevant to train model or logging
                """

        previous_line = ck_line
        # end of: for ck_line in checks_lines:


def get_cks_images_if_not_done_for_this_period():
    if not hasattr(client, "infer_cks_payees"):
        print("  ==>>  NO infer_cks_payees")
        return None
    else:
        print("\n PowerShell ==>> Only one window open ...this client has ck images \n")
        if not this_period_cks_images_done(PERIOD):
            # print("  ==>>  NO this_period_cks_images_done")
            from transactions import extract_cks_images # module is big. only instantiate if is the 1st time. 2nd time, cks images instances are in db
            extract_cks_images.extract_and_save(client_name) # they r saved to db & can not query without a session, so dont keep them in memory 
        return True  
        # else: # no need bc they r saved to db, & need to get them directly from db for any query, since it sqlalchemy uses lazy loading of attributes, we can not keep them in memory, wihtout an open session, may need further research
        #     return get_cks_images_from_db(client_name, period)


def ask_n_show_all_cks_images():
    while True:
        a = red.input(f"\n Do u want to see all cks images ? y/n : ")
        if a == "y" or a == "Y":
            show_all_cks_imgs_for_period(PERIOD)
            return
        if a == "n" or a == "N":
            return

def show_ck_image(ck_number, client_have_cks_imgs):
    if not client_have_cks_imgs:
        print(f"\n Not getting payee image bc this client still does not have the ck_image feature setted up \n")
        return False
    else:
        found, payee_txt_hugginface, payee_txt_textract = show_ck_image_by_ck_number(ck_number)
        activate_powershell()
        if not found:
            red.print(f"\n Did not found payee image for ck# {ck_number}")
            ask_n_show_all_cks_images()
            return False
        else: 
            # we did opened the Photos app to show img
            need_to_close_photos_app = True
            print(f"the vendor infered by hugginface is: {payee_txt_hugginface}")
            print(f"the vendor infered by aws textract is: {payee_txt_textract}")
            # print("\n do NOT continue__________: not coded for images after here")
            return True
        # ask_to_continue()


def print_ck_line(ck_line): 
    red.print("\n=================================")
    red.print("check line:")
    yellow.print(ck_line)
    red.print("=================================\n")

def compare_images_ck_numbers_w_lines_ck_numbers():
    # for ck_line in checks_lines:
    #     ck_number = client.get_ck_number_from_ck_line( ck_line )
    #         if ck_number not in cks_numbers_from_images:
    #             red.print(f"\n Ck number: {ck_number} is in cks lines from bank statement but was not found in the list of cks images extracted")
    #             red.print(f"\n The list of cks numbers from extracted cks images is: ")
    #             red.print(f"{cks_numbers_from_images}\n")
    #             ask_to_continue()
    pass

