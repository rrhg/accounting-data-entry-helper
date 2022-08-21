from config import client
from .order_checks_lines import order_checks_lines

"""
    checks lines are special: 1-do NOT contain vendor. 2-sometimes there are 2 checks in same line
"""

def extract_cks_lines(lines):
    checks_lines = []
    other_lines = []
    previous_line = ''

    
    for line in lines:
        if client.is_a_line_of_checks( line, previous_line ):
            # print('== line bf clean', line)
            line = client.clean_ck_line( line )
            # print('== line after clean', line)
            checks_lines.append( line )
        else:
            other_lines.append( line )
        previous_line = line       

    checks_lines = order_checks_lines( checks_lines )

    return checks_lines, other_lines