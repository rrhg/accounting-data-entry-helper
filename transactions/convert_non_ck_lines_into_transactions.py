from config import client
from .remove_lines import remove_non_debit_lines
import client_partner


def convert_non_ck_lines_into_transactions( non_ck_lines, transactions ):
    previous_line = ''
    non_ck_lines = remove_non_debit_lines( non_ck_lines ) # this uses client.is_not_a_debit_line( line ) to filter

    for line in non_ck_lines:
        if client.do_nothing_but_keep_debit_line( line, previous_line ): # keep line bc may need info from it, like amount (when amount & client_partner are in different lines)
            pass
        else:
            vendor_key = client_partner.find_vendor_in_line_or_ask( line, previous_line )
            if vendor_key: # when is false, user chosed option to ignore line & we dont need to add any transaction
                t = client_partner.get_debit_transaction_from_line( vendor_key, line, previous_line ,ignore_date=False )
                transactions.append( t )
                t.log_and_train( line )

        previous_line = line # even if line was ignored, it is still the previous line & we maight need to get the amount or date from it.