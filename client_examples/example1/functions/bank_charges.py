import re


def there_are_additional_bank_charges_outside_debits_lines():
    return True 
    # return False # for satements where bank charges are in same lines seccion as debits, we do not need this


def line_contains_bank_charges( line ):
    """ only called when there_are_additional_bank_charges_outside_debits_lines () returns True.  Find lines with bank charges, that are not in same seccion with other debits"""
    """ DO NOT INCLUDE HERE BANK CHARGES THAT ARE IN THE SAME LINES SECCION AS OTHER DEBITS """

    if ( 
            'a string' in line
            and bool(re.search('payment', line )) # 
            or
            bool(re.search('^Another string', line )) # start with
            and bool(re.search('^\d\d-\d\d', line )) # starts with date like 01-15
        ):
        return True
    
    return False