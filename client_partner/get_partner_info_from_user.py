from config import vendor, customer
from .get_1_list_of_strings_for_partner import get_1_list_of_strings_for_partner
from rich.console import Console
from transactions.chart_of_accounts import prompt_user_for_account_number
from .partner_dict import partner_dict

red = Console(style="red")
yellow = Console(style="yellow")


def get_partner_info_from_user( ptype=vendor, has_no_code_id=False ):
    vendor_dict = {}
    affects_more_than_1_account = False
    split_amount_in_half = False
    account_can_change = False

    code = ''
    if not has_no_code_id:
        while True:
            red.print(" Enter "+ ptype +" code (max 20 char): " )
            code = red.input(" : " )
            if len(code) > 2 and len(code) <= 20:
                break
    else:
        red.print(f' * * No {ptype} will be created')
        red.print()
    
    name = ''
    while True:
        red.print(" Enter "+ ptype +" name (max 39 char): " )
        name = red.input(" : " )
        if len(name) > 2 and len(name) <= 39:
            break

    memo = ''
    while True:
        red.print(" Enter "+ ptype +" memo (max 30 char): " )
        memo = red.input(" : " )
        if len(memo) > 2 and len(memo) < 31:
            break

    if not has_no_code_id:
        while True:
            red.print("\nAlways 'SPLIT AMOUNT' in half & affect 2 accounts (SS Med) ?" )
            red.print("'n' or 'y' : " )
            a = red.input(" : " )
            if a == 'y' or a == 'Y':
                split_amount_in_half = True
                affects_more_than_1_account = True
                break
            if a == 'n' or a == 'N':
                break

    # use both so it's backwards compatible
    account = ''
    accounts = []

    if not affects_more_than_1_account: # only 1 account for sure
        # do this to maintain backward compatibility
        while True:
            new_account_number = prompt_user_for_account_number()
            if len(new_account_number) > 0:
                account = new_account_number
                break

        if not has_no_code_id:
            while True:
                red.print("\nDoes this account sometimes change ? " )
                a = red.input("'n' or 'y' : " )
                if a == 'y' or a == 'Y':
                    account_can_change = True
                    break
                if a == 'n' or a == 'N':
                    break


    else: # partner affects more than 1 accounts
        while True:
            new_account_number = prompt_user_for_account_number()
            accounts.append( new_account_number )
            break_outer_loop = True

            while True:
                a = red.input("Add another? (y/n): ")
                if a == 'y' or a == 'Y':
                    break_outer_loop = False
                    break
                if a == 'n' or a == 'N':
                    break_outer_loop = True
                    break
                else:
                    pass
            
            if break_outer_loop:
                break


    vtype = '' # vtype == vendor type ; ptype == partner type
    if ptype == vendor and not has_no_code_id:
        while True:
            red.print("\nVendor Type:")
            red.print("Press '[Enter]' for '0'(None) or write '1'(Interest) or '2'(Independent Contractor): " )
            vtype = str( red.input(" : " ) or '0' )
            if vtype in ['0','1','2']:
                break
    else:
        vtype = '0'

    vendor_strings = [] # a list of lists
    vendor_strings.append( code.split() ) # append a list
    vendor_strings.append( name.split() )

    if not has_no_code_id:
        user_strings = get_1_list_of_strings_for_partner( ptype )
        if len( user_strings ) > 0:
            vendor_strings.append( user_strings )
        print()

    d = partner_dict


    d['code']= code
    d['name']= name
    d['memo']=memo
    d['description']=memo
    d['account']= account
    d['account_can_change']= account_can_change
    d['type']= vtype
    d['strings']= vendor_strings
    d['affects_more_than_1_account']= affects_more_than_1_account
    d['accounts']= accounts
    d['split_amount_in_half']= split_amount_in_half

    return d
    # vendor_dict = {
    #     'code': code,
    #     'name': name,
    #     'memo':memo,
    #     'description':memo,
    #     'account': account,
    #     'account_can_change': account_can_change,
    #     'type': vtype,
    #     'strings': vendor_strings,
    #     'affects_more_than_1_account': affects_more_than_1_account,
    #     'accounts': accounts,
    #     'split_amount_in_half': split_amount_in_half,
    # }

