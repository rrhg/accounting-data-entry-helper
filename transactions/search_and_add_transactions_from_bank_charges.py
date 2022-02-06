from utils import lines, dates
import client_partner
from config import client, DATE_END_OF_PERIOD
from rich.console import Console
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

    for line in all_lines:
        """ TODO: this func should be called line_contains_bank_charges_outside_debit_lines()"""

        if client.line_contains_bank_charges( line ): 
            found = True

            red.print('Found a bank charge outside of debits seccion. line : ')
            print(line)
            # a = input('hit enter')
            red.print()
        
            vendor_key = client_partner.find_vendor_in_line_or_ask(line, previous_line, msg_if_not_found='Did not find vendor in bank charges line')

            if vendor_key:
                t = client_partner.get_debit_transaction_from_line( vendor_key, line, previous_line ,ignore_date=False )

                if t:
                    transactions.append( t )
                    t.log_and_train( line, previous_line )
            else:
                pass

        previous_line = line # even if line was ignored temporarily by user, it is still the previous line

    if not found:
        red.print()
        red.print('Did not found any line with bank charges, 🤔, (when searching outside of debits seccion)')
        # print(f'The string "{string_to_find}" in clients/functions/string_in_line_w_total_bank_charges() was not found on any line')
        red.print()
        a = input('Do you want to continue ? y or n : ')
        if a == 'n' or a == 'N':
            exit()
        else:
            pass