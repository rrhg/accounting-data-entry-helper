from utils import lines, dates
import client_partner
from config import client, DATE_END_OF_PERIOD, PATH_FOR_OUTPUT, PERIOD
from rich.console import Console
import config
from utils.other import ask_to_continue


red = Console(style="red")


""" for satements where bank charges are NOT in same lines(section) as debits (& we dont want to add all bank charges lines to lines of debits) """

def search_and_add_transactions_from_bank_charges( all_lines, transactions ):

    # TODO check if this should be deleted bc this function is only called after this returns True in previous function
    # if not client.there_are_additional_bank_charges_outside_debits_lines():
    #     return False

    date_for_charges = DATE_END_OF_PERIOD # bc doesnt have date
    total = 0
    previous_line = ''
    found = False

    charges_for_reconciliation = [] # to create a file with bank charges

    for line in all_lines:
        """ TODO: this func should be called line_contains_bank_charges_outside_debit_lines()"""

        if client.line_contains_bank_charges( line ): 
            found = True

            red.print('Found a bank charge outside of debits seccion. line : ')
            print(line)
            red.print()
        
            vendor_key = client_partner.find_vendor_in_line_or_ask(line, previous_line, msg_if_not_found='Did not find vendor in bank charges line')

            if vendor_key:

                # TODO create vendor_dict somewhere & imported here & get_vendor_dict_from_ck_line & search_and_add_transactions_from_bank_charges
                vendor_dict = {
                    'line_has_2_debits': False,
                    'partner_key': vendor_key,
                    'code': vendor_key,
                    'name': "this will not be used",
                    'amount': "this will not be used",# amount, # this should be a string
                    'ck_number': "this will not be used",# ck_number,
                    'is_check': False, 
                    'date': "this will not be used",#date,
                    #TODO: could ask here for new memo like in get_vendor_dict_from_ck_line
                    'memo': "",# must be "" 
                    'account': "this will not be used",#account,
                    'found': "this will not be used",#True,
                    }            

                # new_transactions = client_partner.get_debit_transaction_from_line( vendor_key, line, previous_line ,ignore_date=False )
                # new_transactions = client_partner.get_debit_transaction_from_bank_charge_line( vendor_key, line, previous_line ,ignore_date=False )
                new_transactions = client_partner.get_debit_transaction_from_bank_charge_line( vendor_dict, line, previous_line ,ignore_date=False )
                if new_transactions: # sometimes amount == 0 & the line is been ignored
                    for t in new_transactions:
                        transactions.append( t )
                        t.log_and_train( line, previous_line )
                        charges_for_reconciliation.append([t.date, t.amount])
            else:
                pass

        previous_line = line # even if line was ignored temporarily by user, it is still the previous line

    # # if hasattr(client, 'create_charges_file_for_reconciliation'):
    # if hasattr(client, 'get_bank_charges_for_external_reconciliation'):
    #     client.get_bank_charges_for_external_reconciliation( charges_for_reconciliation, config)

    if not found:
        red.print()     
        red.print('Did not found any line with bank charges, 🤔, (when searching outside of debits seccion)')
        # print(f'The string "{string_to_find}" in clients/functions/string_in_line_w_total_bank_charges() was not found on any line')
        red.print()
        ask_to_continue()
        # a = input('Do you want to continue ? y or n : ')
        # if a == 'n' or a == 'N':
        #     exit()
        # else:
        #     pass