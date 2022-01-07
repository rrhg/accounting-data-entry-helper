import re
from utils.lines.line_start_w_date_allow_Oo import line_start_w_date_allow_Oo


def get_amount_str_from_credit_line(line):
    return line.split()[-1]



def get_date_str_from_credit_line(line):
    return line.split()[0]



def is_not_a_credit_line(line):
    """ sometimes there are lines that we would like to be automatically removed from the credits section. AKA for these lines, the system won't even ask if user wants to ignore them. """
    # if (     "a string" in line and "another" in line
    #          or
    #          "EFT" in line and 'payment' in line and "returned" in line
    #          or
    #          "another string" in line and 'Cr' in line and 'another' in line
    #    ):
    #     return True
    """ return False if there are not lines to remove in credits section"""
    return False



def is_1st_line_of_credits(line, previous_line):
    if ( 
        (   'str1' in line
            and 'str2' in line
            and 'str3' in line
            and 'str4' in line
            and 'str5' in previous_line
            # len( line.split() ) < 2
        )
        #  or
        #  (
        #      'a string' in line
        #      and 'str2' in line
        #      and 'str3' in previous_line
        #  )
        
        ):

        return True
    
    return False




def is_last_line_of_credits(line, previous_line):
    if ( 
            'str1' in line and 'str2' in line and 'str3' in line
            and
            'str1' in previous_line and 'str2' in previous_line and 'str3' in previous_line
            # len( line.split() ) < 2
        ):

        return True
    
    return False



def do_nothing_but_keep_credit_line( line, previous_line ):
    """
        Credit lines to keep bc contains amount(or date or ...) of next line
        but don't do nothing with it ( as in don't ask if it contains a vendor )
    """
    # return False # if client statement does not have credit lines to jump over(keep but ignore)
    if ( 
            # examples
            # bool(re.search('str1', line )) # 
            # bool(re.search('str1', line, re.IGNORECASE )) # 
            # bool(re.search('^\d\d-\d\d', line )) # starts with date like 01-15
            # and
            
            line_start_w_date_allow_Oo(line)
            and
            bool(re.search('a string', line, re.IGNORECASE ))
            and 'str' in line
            or 
            bool(re.search('a string', line, re.IGNORECASE ))
            and 'str' in line
            or
            'str1' in line and 'str2' in line and 'str3' in line

        ):
        return True
    
    return False



def amount_is_in_previous_credit_line(line, previous_line):
    """
        Sometimes a debit info takes 2 statement lines & the vendor is in the 2nd line while the amount is the previous line
    """
    # return False # if debit info is in the same line(just 1 line per debit), in all debits

    if (
            # line_start_w_date_allow_Oo( line )
            # and
            (    'str1' in line
                 or
                 'str2' in line
                 or
                 'str3' in line
                 or
                 'str4' in line and 'str2' in previous_line
                #  or
                #  'str4' in line
                #  or
                #  'str4' in line
                #  or
                #  'str4' in line
            )
    ):
        return True

    return False



def date_is_in_previous_credit_line(line, previous_line):
    if amount_is_in_previous_credit_line(line, previous_line):
        return True
    return False