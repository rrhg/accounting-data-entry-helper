import re
from utils.strings import try_convert_amount_to_float
from utils.lines.decode_lines import decode_lines
from utils.lines.line_contains_all_strings import line_contains_all_strings
from .bank_charges import line_contains_bank_charges


def get_credits_total_from_statement(statement_text_file):
    from_statement = []
    total = 0
    previous_line = ''
    found_deposits_total = False
    found_transfers_total = False

    lines = decode_lines( statement_text_file )

    for line in lines:
        """ find the line with "Deposits Total"     """
        if (       
                   bool(re.search('^\d\d', line ))
                   and 'string1' in line
                   and 'another' in previous_line
                   and found_deposits_total == False
            ):
            amount_str = line.split()[-1]
            #TODO this code is duplicated
            amount_int = try_convert_amount_to_float(amount_str, amount_str, line=line, caller='client functions compare_totals.py get_credits_total_from_statement()')
            total += amount_int
            found_deposits_total = True # only find one
        elif 'a string' in line and 'another' in previous_line and found_transfers_total == False:
            amount_str = line.split()[-1]
            amount_int = try_convert_amount_to_float(amount_str, amount_str, line=line, caller='client functions compare_totals.py get_credits_total_from_statement()')
            total += amount_int
            found_transfers_total = True # only find one
            # print('Total credits == ', amount_int)
            # a = input('enter')
        previous_line = line

    return round( total, 2 )    



def get_debits_total_from_statement(statement_text_file):
    from_statement = []
    total = 0
    previous_line = ''
    found_debits_total = False
    found_bank_charges_total = False

    lines = decode_lines( statement_text_file )

    for line in lines:
        if (
            bool(re.search('a string', line ))
            and 'another' in previous_line
            and 'other' in previous_line
            and found_debits_total == False
            ):
            amount_str = line.split()[-1]
            amount_int = try_convert_amount_to_float(amount_str, amount_str, line=line, caller='client functions compare_totals.py get_debits_total_from_statement()')
            total += amount_int
            found_debits_total = True # only find one
            # print('Total debits == ', amount_int)
            # a = input('enter')
        elif 'a string' in line and 'another' in previous_line and found_bank_charges_total == False:
            amount_str = line.split()[-1]
            amount_int = try_convert_amount_to_float(amount_str, amount_str, line=line, caller='client functions compare_totals.py get_debits_total_from_statement()')
            total += amount_int
            found_bank_charges_total = True # only find one
            # print('Total debits == ', amount_int)
            # a = input('enter')
        previous_line = line

    return round( total, 2 )