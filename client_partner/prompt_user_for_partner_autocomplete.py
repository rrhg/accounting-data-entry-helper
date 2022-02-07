from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .get_all import get_all
from config import vendor, customer, partner_code, partner_name, partner_account, partner_description, partner_memo, partner_strings
from .get_1_list_of_strings_for_partner import get_1_list_of_strings_for_partner
from config import VENDORS_JSON_FILE, CUSTOMERS_JSON_FILE
from .update_partner import update_partner
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


def prompt_user_for_partner_autocomplete( reason, ptype=vendor ):
    partners_dict = get_all( ptype=ptype ) # get a new one in case it has new vendors or customers
    key = ''

    while True:
        completer = WordCompleter( partners_dict.keys() )
        print()
        red.print("Enter "+ ptype +" for ==> " +  reason )
        key = prompt(" : ", completer = completer)
        print()

        if key in partners_dict:
            break

    """
        Give user the option to add strings to this partner, so that next time, it won't ask
        If we got here is bc user thinks the client_partner exist, but the script did not found the partner
    """
    if key != 'create new vendor' or key != 'create new customer':
        user_strings = get_1_list_of_strings_for_partner(ptype)
        if len( user_strings ) > 0:
            update_partner( key, strings_list=user_strings, ptype=ptype, utype=partner_strings )
    return key
