from config import ENTERED_CHECKS_FILE, client
from utils.entered_checks import ck_was_already_entered, get_already_entered_ck_info, add_to_entered_checks, get_trans_from_vendor_dict
from client_partner import get_debit_transaction_from_check_line
from client_partner import get_vendor_dict_from_ck_line


def convert_checks_lines_into_transactions( checks_lines, transactions ):
    ck_nums_found = []

    for ck_line in checks_lines: 
        ck_number = client.get_ck_number_from_ck_line( ck_line )


        if ( client.use_only_the_1st_ck_when_duplicated()
             and
             ck_number in ck_nums_found
        ):
            print()
            print(f'Ignoring ck# {ck_number} because it was already added & the client function use_only_the_1st_ck_when_duplicated() is set to True')
            print()


        else:
            ck_nums_found.append(ck_number)
            vendor_dict = {}

            if ck_was_already_entered( ck_number, ENTERED_CHECKS_FILE):
                vendor_dict = get_already_entered_ck_info( ck_number, ENTERED_CHECKS_FILE)
            else:
                vendor_dict = get_vendor_dict_from_ck_line( ck_line )
                add_to_entered_checks( vendor_dict, ENTERED_CHECKS_FILE )


            trans = get_trans_from_vendor_dict( vendor_dict )
            transactions.append( trans )

            """ 
                Not training model with checks lines (for now) bc it seems that check lines are not relevant to find the vendor. That's why we ask the user to enter the vendor for each check. Check line only have ck number, date, & those do not tell us anything about the vendor
                trans.log_and_train( ck_line, "" ) # previous line in cks is not relevant to train model or logging
            """
