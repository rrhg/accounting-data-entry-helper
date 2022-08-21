import re
from datetime import datetime
from config import YEAR_FOR_DATE, DATE_END_OF_PERIOD, client
from utils.strings import replace_char_by_index
from utils.lines.line_start_w_date_allow_Oo import line_start_w_date_allow_Oo



def try_convert_date( date_str, line ):
    new = convert_date( date_str, line )
    if new:
        return new

    while True:
        print()
        a = input('Enter a valid date : ')
        new = convert_date( a, line )
        if new:
            return new


def convert_date(old_date, line ):

    new_date = False

    """ lets replace O or o with 0 when at begining of date bc may have been just a mistake of terassac when converting pdf to txt """
    if ( bool(re.search('^O', old_date )) or bool(re.search('^o', old_date )) ):
        old_date = replace_char_by_index( old_date, '0', 0) 
  
    # TODO should this be in client function ? format formats date format
    formats_to_try = [ "%m/%d", "%m/%d/%y", "%m/%d/%Y", "%m-%d", "%m-%d-%y", "%m-%d-%Y" ]

    for f in formats_to_try:
        try:
            new_date = datetime.strptime( old_date, f ).replace( year=int(YEAR_FOR_DATE) )
            break
        except Exception as e:
            new_date = False

    if not new_date:
        if client.use_end_of_period_for_all_trans_w_date_errors():
            return DATE_END_OF_PERIOD
        else:            
            print()
            print( ' Could not convert date. The str was ==> ', old_date )
            print( ' the line was ==>  ', line )
            print('Acepted formats are ==> ', '"mm/dd", "mm/dd/YY", "mm-dd", "mm-dd-YY"')
            print()
            return False
    else: # we have a valid date
        new_date = make_sure_returned_date_has_correct_month(new_date)
        return new_date.strftime('%m/%d/%Y')


def make_sure_returned_date_has_correct_month(to_verify):
    date_w_correct_month = datetime.strptime(DATE_END_OF_PERIOD, "%m/%d/%Y")
    correct_month = date_w_correct_month.strftime('%m')
    current_date_month = to_verify.strftime('%m')
    if not correct_month == current_date_month:
        return to_verify.replace(month=int(correct_month))
    return to_verify


""" code that might be useful here
import calendar
from datetime import datetime
FORMAT = "%m/%d/%Y"    # format accepted by Peachtree. # y == 2 digits year, Y == 4 digits year
def get_first_day( period ):
    y = period.split('/')[-1]
    m = period.split('/')[0]
    date = datetime.date( int(y), int(m), 1)
    # date = datetime.strptime(period, "%m/%d/%Y") # Create date object in given time format mm/dd/yyyy 
    # first = date.replace(day = 1)
    first_str = date.strftime( FORMAT ) 
    return first_str
def get_last_day( period ):
    y = period.split('/')[-1]
    m = period.split('/')[0]
    date = datetime.date( int(y), int(m), 1)
    # date = datetime.strptime(period, "%m/%d/%Y") # Create date object in given time format mm/dd/yyyy
    last = date.replace(day = calendar.monthrange(date.year, date.month)[1]) # replace the day number with the total number of days in that month.
    last_str = last.strftime( FORMAT ) 
    return last_str
"""