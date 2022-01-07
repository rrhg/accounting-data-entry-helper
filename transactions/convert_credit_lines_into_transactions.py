from config import client, vendor, customer
from .remove_lines import remove_non_credit_lines
import client_partner


def convert_credit_lines_into_transactions( found_lines, transactions ):
    previous_line = ''

    """  this use client.is_not_a_credit_line( line ) to filter """
    found_lines = remove_non_credit_lines( found_lines )

    for line in found_lines:
        if client.do_nothing_but_keep_credit_line( line, previous_line ): # keep line bc may need info from it, like amount (when amount & client_partner are in different lines)
            pass
        else:
            customer_key = client_partner.find_customer_in_line_or_ask(line, previous_line)
            if customer_key: # when is false, user chosed option to ignore line & we dont need to add any transaction
                t = client_partner.get_credit_transaction_from_line( customer_key, line, previous_line ,ignore_date=False )
                transactions.append( t )
                t.print_trans_added( line )
        previous_line = line # even if line was ignored, it is still the previous line & we maight need to get the amount from it.