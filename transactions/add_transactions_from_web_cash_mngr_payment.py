import utils
from utils import lines, dates
from utils.strings import try_convert_amount_to_float
import config
from config import client


# TODO delete ??
# maybe this file can be deleted


def add_transactions_from_web_cash_mngr_payment(vendor_key, line, previous_line, transactions_dicts_list):

    total_amount_float = try_convert_amount_to_float( previous_line.split()[-1], previous_line, caller='debits.add_transactions_from_web_cash_mngr_payment()' ) # in case the pdf was read incorrectly & the amount includes unrecognized characters

    total_amount_str = previous_line.split()[-1]
    applied_amount = 0
    date = previous_line.split()[0]
    date = dates.try_convert_date( date, line )
    ck_number = 'web cash mg'
    is_check = False

    def add_transaction(transactions_dicts_list, vendor_key, edit=False):
        nonlocal total_amount_float, total_amount_str ,applied_amount, date, ck_number, is_check 

        """ TODO : = client_partner.get_all() """
        print('need to fix transactions/add_transactions_from_web_cash_mngr_payment. Exiting !!!!')
        exit()
        # vendors_dict = vendors.get_vendors_dict() # get a new one in case has new vendors
        vendors_dict = {}

        account = vendors_dict[vendor_key]['account']
        memo = vendors_dict[vendor_key]['description']
        amount = total_amount_str
        if edit == True:
            new_memo = input("Enter memo: (Leave Blank to use vendor description) :")
            if new_memo != "": # If user enters something, then use it as memo
                memo = new_memo
            amount = str( input(" Amount : ") )

            # applied_amount += to_int(amount)
            applied_amount = try_convert_amount_to_float( amount, 'entered by user' ) # in case the pdf was read incorrectly & the amount includes unrecognized characters
        
        # info = {'vendor': vendor, 'amount': amount, 'ck_number': ck_number, 'is_check': is_check, 'date': date, 'memo': memo, 'account': account}
        # lines.append(info)
        vendor_dict = {
            'line_has_2_debits': False,
            'vendor_key': vendor_key,
            'amount': amount, # this should be a string
            'ck_number': 'web cash mgr',
            'is_check': False,
            'date': date, 
            'memo': memo, 
            'account': account,
            'found': True
            }

        transactions_dicts_list.append( vendor_dict )             

    a = input("Are you going to change this transaction? y/n -> " + vendor_key + " -> Date == " + date + " ; Total == " + str(total_amount_str) + " : "  )
    if a == 'n' or a == 'N':
        add_transaction(transactions_dicts_list, vendor_key, edit=False)
    else:
        while True:
            a = input("Add another transaction? y/n -> Web Cash Mngr Payment -> Date == " + date + " ; Total == " + str(total_amount_float) + " ; applied == " + str(applied_amount) + " ; diff == " + str( (total_amount_float - applied_amount) ) + " : "  )
            if a == 'y' or a == 'Y':

                """ TODO vendors now is client_partner """
                # vendor_key = vendors.prompt_user_for_vendor_autocomplete('Web Cash Mngr Payment')
                vendor_key = ""
                

                if vendor_key == 'create new vendor':
                    # vendor_info_dict = vendors.create_and_add_vendor( '' ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a web cash line we dont have vendor info
                    # vendor_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }

                    # vendor_key = vendor_info_dict['code'] 
                    vendor_key = ""

                add_transaction(transactions_dicts_list, vendor_key, edit=True)
            else:
                break

