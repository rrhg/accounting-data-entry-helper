from rich.console import Console
from config import ( 
    client, customer, vendor,
    REFERENCE_FOR_DEBITS_THAT_ARE_NOT_CHECKS,
    INTERNAL_PERIOD_NUMBER
)
from utils.strings import try_convert_amount_to_float
from utils.dates import try_convert_date
from transactions.transaction import transaction
from transactions.transaction import transaction_type as ttype
from .get_all import get_all
from .create_and_add_partner import create_and_add_partner
from transactions.chart_of_accounts import (
    prompt_user_for_account_number, get_account_name
)
from client_partner.get_partner_info_from_user import get_partner_info_from_user



def get_credit_transaction_from_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ptype=customer, ignore_date=ignore_date )

def get_debit_transaction_from_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ttype=ttype.other, ptype=vendor, ignore_date=ignore_date )

def get_debit_transaction_from_check_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ttype=ttype.check, ptype=vendor, ignore_date=ignore_date, is_check = True )

def get_debit_transaction_from_bank_charge_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ttype=ttype.bank_charge, ptype=vendor, ignore_date=ignore_date, is_check = True )


def get_transaction_from_line( partner_key, line, previous_line, ttype='' ,ptype=vendor, ignore_date=False, is_check = False ):

    # print(f"\n line received in get_transaction_from_line(): {line}")

    def main():
        if split_amount_in_half:
            create_splited_transactions()
        elif affects_more_than_1_account:
            create_many_trans()
        elif account_can_change and not affects_more_than_1_account:
            create_1_trans( change_account=True)
        else: # only 1 account doesn't change
            create_1_trans( change_account=False)
        # print(new_transactions)
        return new_transactions

    new_transactions = []
    amount = ''
    date = ''
    ck_number = REFERENCE_FOR_DEBITS_THAT_ARE_NOT_CHECKS
    splited = line.split()
    red = Console(style="red")

    all_partners = get_all( ptype=ptype ) # get a new one in case it has new vendors

    if partner_key == 'do not create new vendor':
        partner_dict = get_partner_info_from_user(has_no_code_id=True)
    else:
        partner_dict = all_partners[ partner_key ]
    

    partner_code =        partner_dict['code']
    partner_name =        partner_dict['name']
    memo =                partner_dict['description']
    account =             partner_dict['account']
    account_can_change=   partner_dict.get('account_can_change', False)
    affects_more_than_1_account = partner_dict.get('affects_more_than_1_account', False)
    accounts =            partner_dict.get('accounts', False)
    split_amount_in_half= partner_dict.get('split_amount_in_half', False)

    bank_account = client.get_bank_account()

    amount_is_in_previous_line = client.amount_is_in_previous_debit_line
    date_is_in_previous_line = client.date_is_in_previous_debit_line
    get_amount_from_line = client.get_amount_str_from_debit_line
    get_date_from_line = client.get_date_str_from_debit_line

    if ptype == customer:
        amount_is_in_previous_line = client.amount_is_in_previous_credit_line
        date_is_in_previous_line = client.date_is_in_previous_credit_line
        get_amount_from_line = client.get_amount_str_from_credit_line
        get_date_from_line = client.get_date_str_from_credit_line

    if is_check == True:
        get_amount_from_line = client.get_amount_str_from_ck_line
        ck_number = client.get_ck_number_from_ck_line(line)
        get_date_from_line = client.get_date_from_ck_line

        # verify_ck_numb_is_in_ck_imgs()



    amount_line = line
    if amount_is_in_previous_line(line, previous_line, is_check=is_check):
        # print(f"amount_is_in_previous_line")
        amount_line = previous_line
    # else:
    #     print('amount is not inprevious line')

    # print(f"\n amount_line in get_transaction_from_line(): {amount_line}\n")


    amount = get_amount_from_line( amount_line )
    """ Lets check if amount can be converted now. Bc if pdf2txt conversion made a mistake, is better to ask user now to correct amount, bc later it will be used in many other functions"""
    amount = try_convert_amount_to_float( amount, splited, line=amount_line ,caller='client_partner.get_partner_dict_from_line()' ) # in case the pdf was read incorrectly & the amount includes unrecognized characters
    """ In some statements, bank charges lines are printed even if have a 0.00 amount """
    if amount == 0:
        print()
        red.print('Ignoring line because amount == 0. Line was:')
        print(amount_line)
        print()
        return [] # ignoring line
    amount = str( amount )


    date_line = line
    if date_is_in_previous_line(line, previous_line, is_check=is_check):
        date_line = previous_line
        
    if ignore_date == False:
        date = get_date_from_line( date_line )
        date = try_convert_date( date, date_line )
    else: # just use end of period date. ignore_date was true. Maybe statement lines do not have dates 
        date = config.DATE_END_OF_PERIOD


    def create_many_trans():
        # print(f"line ==> {line}")
        for number in accounts:
            if account_can_change:
                number = get_new_account(number)

            name = get_account_name(number)
            red.print(f"\nEnter 'amount' for account '{number}' {name} : ")
            a = red.input(f"Write '0' or press '[Enter]' to 'skip' : ") or 0
            if a == 0 or a == '0' or a == '':
                pass # ignore / skip; user does not want to use this account
            else:
                create_and_add_trans( number, str(a) )


    def create_splited_transactions():
        red.print("\nThis Partner has 'split_amount' set to true.")
        red.print("Do u want to split amount in 2 accounts?")
        red.print(f"Partner: {partner_name}")
        red.print(f"Line: {line}")
        red.print(f"Previous Line: {previous_line}")
        a = red.input("Press '[Enter]'(yes) or 'n'(No) ")
        if a == 'n' or a == 'N':
            create_many_trans()
        else:
            if len(accounts) < 2:
                raise Exception('Vendor has less than 2 accounts. With spli_amounts_in_half it should have 2 or more accounts(for now). Unless is refactored')

            half_1 = round(( float(amount)/2), 2)
            half_2 = round( float(amount) - half_1, 2)

            # amounts should be strings
            create_and_add_trans(accounts[0], str(half_1)) 
            create_and_add_trans(accounts[1], str(half_2)) 


    def create_1_trans( change_account=False):
        if change_account:
            acc = get_new_account(account)    
        else:
            acc = account
        create_and_add_trans(acc, amount)


    def get_new_account(number):
        name = get_account_name(number)
        full_name = f"{number} {name}"

        red.print("\nAccount for this partner sometimes change")
        red.print(f"partner: {partner_name}")
        red.print(f"line: {line}")
        red.print(f"previous line: {previous_line}")
        red.print(f"Account is {full_name}")
        while True:
            red.print("Do u want to change it")
            a = red.input("'n' or 'y' : ")
            if a == 'n' or a == 'N':
                return number
            if a == 'y' or a == 'Y':
                break
        while True:
            new_account_number = prompt_user_for_account_number()
            return str(new_account_number)


    def create_and_add_trans(account, amount):
        t = transaction()
        t.account = account
        t.amount = amount
        t.partner_key = partner_key
        t.partner_code = partner_code
        t.partner_name = partner_name
        t.ck_number = ck_number
        t.ttype = ttype
        t.is_check = is_check 
        t.date = date 
        t.memo = memo 
        t.bank_account = bank_account
        t.internal_period_number = INTERNAL_PERIOD_NUMBER
        new_transactions.append(t)


    return main()