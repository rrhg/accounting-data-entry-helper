import re


"""
    Checks lines are special: 1-do NOT contain vendor. 2-sometimes there are 2 checks in same 
"""


def is_a_line_of_checks(line, previous_line):
    # return False # when there are no checks(that need to enter vendor manually). Or for testing without entering checks

    if ( 
            'a string' in line
            and bool(re.search('^000000', line )) 
            and bool(re.search('\d\d-\d\d', line ))
            or
            'another' in previous_line
            and len( line.split() ) < 2
        ):
        return True
    
    return False


    
def get_1st_ck_line_from_line( line ):
    """  
        A check line may contain more than 1 check.
        Here we get only the info(line aka string) from the 1st one.
    """
    # return line # if there is only 1 check per line

    splited = line.split()
    ck1 = splited[:4] # in this case, 1st check info is in 1st 4 words of the line
    ck1 = ' '.join(ck1) # bc next functions expect lines to be strings
    return ck1



def get_2nd_ck_line_from_line( line ):
    """  
        A check line may contain more than 1 check.
        Here we get only the info(line aka string) from the 2nd check.
    """
    splited = line.split()
    ck2 = splited[4:]
    ck2 = ' '.join(ck2) # bc next functions expect lines to be strings
    # print('ck2 == ', ck2)
    return ck2



def get_amount_str_from_ck_line( ck_line ):
    splited = ck_line.split()
    amount = splited[-1]
    return amount



def get_ck_number_from_ck_line( ck_line ):
    splited = ck_line.split()
    ck_number = splited[0][6:]
    return ck_number



def get_date_from_ck_line( ck_line ):
    splited = ck_line.split()
    date = splited[1]
    return date



def line_has_more_than_1_ck( line ): 
    if len( re.findall( '\d\d-\d\d\s', line )    ) > 1: # theres 2 checks on same line. need to get the other check info
        return True
    return False


def clean_ck_line( line ):
    return line.replace(" * ", " ").replace(" - ", " ").replace(" _ ", " ") # sometimes the line has u helpful *, & sometimes pdf2txt confuses it for a - or a _
    # return line # when no need to clean a check line

def use_only_the_1st_ck_when_duplicated():
    # return False

    """
       Sometimes returned checks that were re deposited 
       appear twice in a bank statement
       Here you have the option ignore them & only the 
       first check will be added to transactions in the output csv file
    """
    return True #  