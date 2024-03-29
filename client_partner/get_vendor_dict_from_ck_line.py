
from config import client, vendor
from utils.strings import try_convert_amount_to_float
from utils.dates import try_convert_date
from utils.other import ask_to_continue
from .prompt_user_for_partner_autocomplete import prompt_user_for_partner_autocomplete
from .create_and_add_partner import create_and_add_partner
from .get_all import get_all
from db.cks_images import get_infered_payee_from_ck_image
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


# TODO: No delete but: 
#           Think should be named get_or_created_vendor bc maybe thas the only thing used from it
#                see transactions / convert_checks_lines_into_transactions


def get_or_create_vendor_dict_from_ck_line( 
                       ck_line,
                       ck_number,
                       client_have_cks_imgs,
                       found_ck_image,
                       ask_n_show_all_cks_images,
                        ):
    # TODO: maybe no need to get amount, date, ck number herebc is been done in get transaction from line 
    amount = client.get_amount_str_from_ck_line( ck_line )
    """ in case the pdf was read incorrectly & the amount includes unrecognized characters, ask to fix it here, instead of getting an error later """
    amount = try_convert_amount_to_float( amount, ck_line, line=ck_line, caller='client_partner.get_or_create_vendor_dict_from_ck_line()' )
    amount = str( amount )
    date = client.get_date_from_ck_line( ck_line )
    date = try_convert_date( date, ck_line)


    # previously we automatiacally prompted for a vendor
    # vendor_key = prompt_user_for_partner_autocomplete(ck_number)

    # but now we do it like non check lines
    #    1- search for a vendor w strings that match infered payee
    #    2- if not ask to :choose(prompt) vendor, ignore, etc
    infered_payee = get_infered_payee_from_ck_image(ck_number)
    previous_line = ""

    def get_vendor_key(): # TODO circular dependency
        from client_partner.find_in_line_or_ask import find_vendor_in_line_or_ask
        vendor_key = find_vendor_in_line_or_ask(
            ck_line,
            previous_line,
            is_check=True, 
            infered_payee_in_ck_image=infered_payee
        )
        return vendor_key

    vendor_key = get_vendor_key()


    # not anymore. now done in previous function
    # if vendor_key == 'create new vendor':
    #     # vendor_info_dict = create_and_add_partner( '' ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
    #     vendor_info_dict = create_and_add_partner( ck_line, 'no previous line available' ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
    #     # vendor_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
    #     vendor_key = vendor_info_dict['code'] 

    vendors_dict = get_all( ptype=vendor ) # get a new one bc we just added a new vendor_key

    vendor_name = vendors_dict[vendor_key]['name']
    account = vendors_dict[vendor_key]['account']
    memo = vendors_dict[vendor_key]['description']

    print(f"\n vendor found for ck#{ck_number} is:")
    print(f"{vendor_name} \n")

    red.print("\nEnter memo: (Leave Blank to use vendor description) :")
    new_memo = input(" : ")
    if new_memo != "": # If user enters something, then use it as memo
        memo = new_memo 

    # TODO should import vendor_dict or partner dict from client_partner
    vendor_dict = {
        'line_has_2_debits': False,
        'partner_key': vendor_key,
        'code': vendor_key,
        'name': vendor_name,
        'amount': amount, # this should be a string
        'ck_number': ck_number,
        'is_check': True, 
        'date': date, 
        'memo': memo, 
        'account': account,
        'found': True,
        }

    return vendor_dict
