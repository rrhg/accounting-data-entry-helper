import re
from datetime import datetime


def line_start_w_date_allow_Oo(line):
    # TODO should we check for all accepted formats ? these are accepted formars in utils.dates...
    # formats_to_try = [ "%m/%d", "%m/%d/%y", "%m/%d/%Y", "%m-%d", "%m-%d-%y", "%m-%d-%Y" ]
    # should this be in client function ? format formats date format

    def check_for_full_date(line):
        try:
            return bool(datetime.strptime( line.split()[0], "%m/%d/%Y") ) # Create date object in given time format mm/dd/yyyy # this throws an error if can't find formated date
        except:
            return False        

    def check_for_month_day_date(line):
        try:
            return bool(datetime.strptime( line.split()[0], "%m/%d") ) # Create date object in given time format mm/dd/yyyy # this throws an error if can't find formated date
        except:
            return False

    if ( 
            ( 
              bool(re.search('^\d\d-\d\d', line ))
              or
              bool(re.search('^O\d-\d\d', line )) # includes when 0 is an O
              or
              bool(re.search('^O\d-O\d', line )) # includes when 0 is an O
              or
              bool(re.search('^o\d-o\d', line )) # includes when 0 is an O
              or
              bool(re.search('^o\d-\d\d', line )) # includes when 0 is an O
              or
              bool(re.search('^Q\d-\d\d', line )) # includes when 0 is an O
              or
              bool(re.search('^Q\d-Q\d', line )) # includes when 0 is an O
              or
              check_for_full_date(line)
              or
              check_for_month_day_date(line)

            )
    ):
        return True

    return False

""" code that might be useful here
import calendar
import datetime
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