from config import client

"""  
    This is useful in statements where debits & credits are mixed 
    aka there is no diferent seccions for debits & credits
    & we would like to NOT include credit lines when working with debit lines, & viceversa.    
"""

# TODO use list comprehensions
def remove_non_debit_lines(lines):
    new_list = []
    for l in lines:
        if client.is_not_a_debit_line( l ):
            pass
        else: # is a debit line
            new_list.append( l )
    return new_list

def remove_non_credit_lines(lines):
    new_list = []
    for l in lines:
        if client.is_not_a_credit_line( l ):
            pass
        else: # is a credit line
            new_list.append( l )
    return new_list