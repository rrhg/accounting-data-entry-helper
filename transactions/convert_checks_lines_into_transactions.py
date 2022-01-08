from config import ENTERED_CHECKS_FILE, client
from utils.entered_checks import ck_was_already_entered, get_already_entered_ck_info, add_to_entered_checks, get_trans_from_vendor_dict
from client_partner import get_debit_transaction_from_check_line
from client_partner import get_vendor_dict_from_ck_line


def convert_checks_lines_into_transactions( checks_lines, transactions ):

    for ck_line in checks_lines: 
        ck_number = client.get_ck_number_from_ck_line( ck_line )
        vendor_dict = {}

        if ck_was_already_entered( ck_number, ENTERED_CHECKS_FILE):
            vendor_dict = get_already_entered_ck_info( ck_number, ENTERED_CHECKS_FILE)
        else:
            vendor_dict = get_vendor_dict_from_ck_line( ck_line )
            add_to_entered_checks( vendor_dict, ENTERED_CHECKS_FILE )

        trans = get_trans_from_vendor_dict( vendor_dict )
        transactions.append( trans )
        trans.print_trans_added( ck_line )