from utils.json import get_dict_from_json_file
from utils.json import write_dict_to_json_file
from .create_if_no_entered_cks_file import create_if_no_entered_cks_file
from transactions.transaction import transaction
from config import client, INTERNAL_PERIOD_NUMBER

def get_already_entered_ck_info( ck_number, ENTERED_CHECKS_FILE ):

    create_if_no_entered_cks_file( ENTERED_CHECKS_FILE )

    dict_of_dicts = get_dict_from_json_file( ENTERED_CHECKS_FILE )

    for entered_ck_number in dict_of_dicts.keys():
        if ck_number == entered_ck_number:
            return dict_of_dicts[entered_ck_number]
            # print(ck_number + ' was alreadyentered')

    print(' error ====>  did not find ck number in utils.entered_checks.get_already_entered_ck_info()')
    exit()
    # return False

# def get_trans_from_vendor_dict( vendor_dict ):
#     bank_account = client.get_bank_account()
#     d = vendor_dict
#     t = transaction()

#     t.partner_key = d['vendor_key']
#     t.partner_code = d['vendor_key']
#     t.partner_name = d['name']
#     t.amount = d['amount']
#     t.ck_number = d['ck_number']
#     t.is_check = d['is_check'] 
#     t.date = d['date']
#     t.memo = d['memo']
#     t.account = d['account']
#     t.bank_account = bank_account
#     t.internal_period_number = INTERNAL_PERIOD_NUMBER

#     return t