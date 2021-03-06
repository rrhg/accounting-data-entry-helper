import re
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


def start_w_dollar_sign(string):
    return bool(re.search('^\$', string ))


def replace_char_by_index(s, char, index):
    return s[:index] + char + s[index +1:]


def clean_line_for_training(line):
    """ remove non important strings for training the model """
    line = re.sub(r'\s+', ' ',   line) # Eliminate duplicate whitespaces using wildcards
    
    # 1st look complete date that uses /
    line = re.sub(r"\d+/\d+/\d+", '',   line) # complete date
    # then without year
    line = re.sub(r"\d+/\d+", '',   line) # day & month
    
    line = re.sub(r"\d+-\d+-\d+", '',   line) # complete date
    line = re.sub(r"\d+-\d+", '',   line) # day & month
    
    line = re.sub(r"\d+\.\d+", '',   line) # amounts that have a .
    line = re.sub(r"\.\d+", '',   line) # cents after a .
    line = re.sub(r'\$+', '',   line) # $
    line = re.sub(r'\s-\s', ' ',   line) # space - space
    line = re.sub(r'^\s+', '',   line) # rm whitespaces at beg
    line = re.sub(r'\n+', '',   line)
    line = line.upper()
    line = line.replace('*', '')
    return line


def try_convert_amount_to_float( amount_str_received , transaction_dict, line = '', caller = ''):

    def fix_comma_instead_of_decimal_point(str_amount):
        if bool( re.search(',\d\d$', str_amount) ):
            indexes = [i for i, char in enumerate(str_amount) if char == ',']
            last_comma_index = indexes[-1]
            fixed_amount = str_amount[:last_comma_index] + '.' + str_amount[-2:]
            str_amount = fixed_amount
        return str_amount

    def to_float(s):
        s = s.replace(',','').replace('$', '').replace('-', '')
        # s = "{:.2f}".format( s ) # this was not working.? # add 2 decimals bc if is .00 it was showing only .0 # this returns a string
        f = round( float(s), 2 )
        return f

    corrected_amount_str = fix_comma_instead_of_decimal_point( amount_str_received )

    try:
        amount = to_float( corrected_amount_str )
        return amount
    except:
        print()
        # print( ' could not convert str to float in utils.strings.try_convert_amount_to_float(). The str was ==> ', amount_str_received )
        red.print( ' ==> Could not convert amount to float. The amount was : ')
        print( amount_str_received )
        red.print( ' ==> the transaction was :  ')
        print(transaction_dict)
        if line != '':
            red.print(' ==> line was ==> ')
            print( line)
        # if caller != '':
            # print(' ==> caller function was ==> ', caller)
        print()
        
        while True:
            red.print('Enter a valid amount :')
            a = input(' : ')
            try:
                amount = to_float( a )
                return amount
            except:
                pass
