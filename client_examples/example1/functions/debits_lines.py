import re
from utils.lines.line_start_w_date_allow_Oo import line_start_w_date_allow_Oo



def get_amount_str_from_debit_line(line):
    return line.split()[-1]



def get_date_str_from_debit_line(line):
    return line.split()[0]



def is_not_a_debit_line(line):
    """ sometimes there are lines that we would like to be automatically removed from the debits section. AKA for these lines, the system won't even ask if user wants to ignore them. They will be removed before getting to that point """

    if (     
             "str1" in line and "another" in line
             or
             "str1" in line and 'another' in line and "another" in line
             or
             "str1" in line and 'another' in line and 'another' in line
       ):
        return True

    """ return False if there are no lines to remove in credits section"""
    return False



def is_1st_line_of_debits(line, previous_line):
    if ( 
           ( # a different approach. add more parens
            'str' in line
            and 'another' in previous_line
            and len( line.split() ) < 2
           )
         or
           (
             'another' in line
             and 'str' in previous_line
           )
       ):
        return True
    
    return False



def is_last_line_of_debits(line, previous_line):
    if ( 
            'str' in line
            or
            'str2' in previous_line
            and len( line.split() ) < 2
        ):
        return True
    
    return False



def do_nothing_but_keep_debit_line( line, previous_line ):
    """
    Debit lines to keep bc contains amount of next line
    but don't do nothing with it ( as in don't ask if it contains a vendor )
    """
    if (  
            'str1' in line
            and line_start_w_date_allow_Oo(previous_line)
            or
            bool(re.search('^\d\d-\d\d', previous_line ))
            and bool(re.search('str', previous_line ))
            and bool(re.search('str2', previous_line ))
        ):
        return True
    
    return False



def amount_is_in_previous_debit_line(line, previous_line):
    """
        Sometimes a debit info takes 2 statement lines & the vendor is in the 2nd line while the amount is the previous line
    """
    # return False # if debit info is in the same line(just 1 line per debit), in all debits

    if (
            line_start_w_date_allow_Oo( previous_line )
            and'str' in previous_line
        ):
        return True

    return False
    


def date_is_in_previous_debit_line(line, previous_line):
    if amount_is_in_previous_debit_line(line, previous_line):
        return True
    return False
