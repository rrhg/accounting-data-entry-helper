from config import client, STATEMENT_PDF
from .remove_lines import remove_non_debit_lines
import client_partner
from transactions.ignored_lines import line_is_in_ignored_lines
from utils.gui import activate_edge_n_open_file, activate_powershell

from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


def convert_non_ck_lines_into_transactions( non_ck_lines, transactions ):
    previous_line = ''
    non_ck_lines = remove_non_debit_lines( non_ck_lines ) # this uses client.is_not_a_debit_line( line ) to filter

    activate_edge_n_open_file(str(STATEMENT_PDF))
    activate_powershell()

    for line in non_ck_lines:
        if (  # keep line bc may need info from it, like amount (when amount & client_partner are in different lines)
            client.do_nothing_but_keep_debit_line( line, previous_line )
            or

            # previously this was done bf getting here (when getting lines from statement)
            # but now done here bc some lines are used as previous line
            line_is_in_ignored_lines(line)

        ):
            red.print("=================================")
            red.print("Ignored line:")
            yellow.print(line)
            red.print("=================================")
            pass
        else:

            get_trans = client_partner.get_debit_transaction_from_line
            if client.line_contains_bank_charges(line):
                get_trans = client_partner.get_debit_transaction_from_bank_charge_line 
                # just to mark it as bank charge. aka t.ttype == 'bank_charge'
               
            # print(f"===non ck line: {line}")


            vendor_key = ''
            if (
                hasattr(client, 'vendor_key_for_all_bank_charges')
                and
                client.line_contains_bank_charges(line)
                ):
                vendor_key = client.vendor_key_for_all_bank_charges()

            else:
                vendor_key = client_partner.find_vendor_in_line_or_ask( line, previous_line )

            # maybe: vendor_key == 'no vendor id':
            #  for trans without vendor

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

            if vendor_key: # when is false, user chosed option to ignore line & we dont need to add any transaction

                # new_transactions = get_trans( vendor_key, line, previous_line ,ignore_date=False )
                new_transactions = get_trans( vendor_dict, line, previous_line ,ignore_date=False )
                for t in new_transactions:
                    transactions.append( t )
                    t.log_and_train( line, previous_line )

        previous_line = line # even if line was ignored, it is still the previous line & we maight need to get the amount or date from it.
