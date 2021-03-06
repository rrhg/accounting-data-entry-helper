from config import vendor, customer
from .get_1_list_of_strings_for_partner import get_1_list_of_strings_for_partner
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


def get_partner_info_from_user( ptype=vendor ):
    vendor_dict = {}

    code = ''
    while True:
        red.print(" Enter "+ ptype +" code (max 20 char): " )
        code = input(" : " )
        if len(code) > 2 and len(code) <= 20:
            break
    
    name = ''
    while True:
        red.print(" Enter "+ ptype +" name (max 39 char): " )
        name = input(" : " )
        if len(name) > 2 and len(name) <= 39:
            break

    memo = ''
    while True:
        red.print(" Enter "+ ptype +" memo (max 30 char): " )
        memo = input(" : " )
        if len(memo) > 2 and len(memo) < 31:
            break

    account = ''
    while True:
        red.print(" Enter "+ ptype +" account: " )
        account = input(" : " )
        if len(account) > 0:
            break
    

    vtype = '' # vtype == vendor type ; ptype == partner type
    if ptype == vendor:
        while True:
            red.print(" Enter vendor vtype: only a 0(None) or 1(Interest) or 2(Independent Contractor): " )
            vtype = str( input(" : " ) )
            if vtype in ['0','1','2']:
                break
    else:
        vtype = '0'

    vendor_strings = [] # a list of lists
    vendor_strings.append( code.split() ) # append a list
    vendor_strings.append( name.split() )

    user_strings = get_1_list_of_strings_for_partner( ptype )
    if len( user_strings ) > 0:
        vendor_strings.append( user_strings )
    print()

    # TODO use partner_dict
    vendor_dict = {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': vendor_strings }
    return vendor_dict
