
from config import client, vendor
from utils.strings import try_convert_amount_to_float
from utils.dates import try_convert_date

from .prompt_user_for_partner_autocomplete import prompt_user_for_partner_autocomplete
from .create_and_add_partner import create_and_add_partner
from .get_all import get_all


# TODO: to delete ?? Maybe this file can be deleted


def get_vendor_dict_from_ck_line( ck_line ):
    amount = client.get_amount_str_from_ck_line( ck_line )
    """ in case the pdf was read incorrectly & the amount includes unrecognized characters, ask to fix it here, instead of getting an error later """
    amount = try_convert_amount_to_float( amount, ck_line, line=ck_line, caller='client_partner.get_vendor_dict_from_ck_line()' )
    amount = str( amount )

    ck_number = client.get_ck_number_from_ck_line( ck_line )

    date = client.get_date_from_ck_line( ck_line ) 
    date = try_convert_date( date, ck_line)
   
    vendor_key = prompt_user_for_partner_autocomplete(ck_number)
    # print('vendor_key AFYER prompt user i put == ', vendor_key)
    # print()

    if vendor_key == 'create new vendor':
        # vendor_info_dict = create_and_add_partner( '' ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
        vendor_info_dict = create_and_add_partner( ck_line, 'no previous line available' ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
        # vendor_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
        vendor_key = vendor_info_dict['code'] 

    # vendors_dict = get_vendors_dict() # get a new one bc we just added a new vendor_key
    vendors_dict = get_all( ptype=vendor ) # get a new one bc we just added a new vendor_key

    # vendor_key == 'is_a_check' # for testing without entring all checks payees
    name = vendors_dict[vendor_key]['name']
    account = vendors_dict[vendor_key]['account']
    memo = vendors_dict[vendor_key]['description']
    new_memo = input("Enter memo: (Leave Blank to use vendor description) :")
    if new_memo != "": # If user enters something, then use it as memo
        memo = new_memo 

    # TODO should import vendor_dict or partner dict from client_partner
    vendor_dict = {
        'line_has_2_debits': False,
        'vendor_key': vendor_key,
        'code': vendor_key,
        'name': name,
        'amount': amount, # this should be a string
        'ck_number': ck_number,
        'is_check': True, 
        'date': date, 
        'memo': memo, 
        'account': account,
        'found': True
        }
    return vendor_dict
