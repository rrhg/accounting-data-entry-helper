from config import ( client, customer, vendor,
                     REFERENCE_FOR_DEBITS_THAT_ARE_NOT_CHECKS,
                     INTERNAL_PERIOD_NUMBER )
from utils.strings import try_convert_amount_to_float
from utils.dates import try_convert_date
from transactions.transaction import transaction
from .get_all import get_all
from .create_and_add_partner import create_and_add_partner
from rich.console import Console
red = Console(style="red")


def get_credit_transaction_from_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ptype=customer, ignore_date=ignore_date )

def get_debit_transaction_from_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ptype=vendor, ignore_date=ignore_date )

def get_debit_transaction_from_check_line( partner_key, line, previous_line, ignore_date=False ):
    return get_transaction_from_line( partner_key, line, previous_line, ptype=vendor, ignore_date=ignore_date, is_check = True )


def get_transaction_from_line( partner_key, line, previous_line, ptype=vendor, ignore_date=False, is_check = False ):
        amount = ''
        date = ''
        ck_number = REFERENCE_FOR_DEBITS_THAT_ARE_NOT_CHECKS
        splited = line.split()

        if is_check == True:
            vendor_info_dict = create_and_add_partner( line, previous_line, ptype=vendor ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
            # vendor_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
            partner_key = vendor_info_dict['code'] 

        all_partners = get_all( ptype=ptype ) # get a new one in case it has new vendors
        partner_code = all_partners[ partner_key ]['code']
        partner_name = all_partners[ partner_key ]['name']
        account =      all_partners[ partner_key ]['account']
        memo =         all_partners[ partner_key ]['description']
        account =      all_partners[ partner_key ]['account']
        memo =         all_partners[ partner_key ]['description']

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
            ck_number = client.get_ck_number_from_ck_line
            get_date_from_line = client.get_date_from_ck_line


        amount_line = line
        if amount_is_in_previous_line(line, previous_line):
            amount_line = previous_line
        try:
            amount = get_amount_from_line( amount_line )
            """ Lets check if amount can be converted now. Bc if pdf2txt conversion made a mistake, is better to ask user now to correct amount, bc later it will be used in many other functions"""
            amount = try_convert_amount_to_float( amount, splited, line=amount_line ,caller='client_partner.get_partner_dict_from_line()' ) # in case the pdf was read incorrectly & the amount includes unrecognized characters

            """ In some statements, bank charges lines are printed even if have a 0.00 amount """
            if amount == 0:
                print();red.print('Ignoring because amount == 0. Line was:');print(amount_line);print()
                return False

            amount = str( amount )
        except Exception as e:
            red.print('In the first line, we could not split the previous line. Just pass, for now. Probably not important...');print() # TODO : is this true ?

        date_line = line
        if date_is_in_previous_line(line, previous_line):
            date_line = previous_line
            
        if ignore_date == False:
            date = get_date_from_line( date_line )
            date = try_convert_date( date, date_line )
        else: # just use end of period date. ignore_date was true. Maybe statement lines do not have dates 
            date = config.DATE_END_OF_PERIOD

        t = transaction()
        t.partner_key = partner_key
        t.partner_code = partner_code
        t.partner_name = partner_name
        t.amount = amount
        t.ck_number = ck_number
        t.is_check = is_check 
        t.date = date 
        t.memo = memo 
        t.account = account
        t.bank_account = bank_account
        t.internal_period_number = INTERNAL_PERIOD_NUMBER

        return t
