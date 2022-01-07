import calendar
import datetime


OUTPUT_DATE_FORMAT = "%m/%d/%Y"    # format accepted by Peachtree for dates in csv. # y == 2 digits year, Y == 4 digits year


def get_periods():
    """ No need to change this, unless you want a different period format & are willing to spend some time fixing other functions where this format is used. Because it will break some stuff """
    """ 
        returns {'2020-01': '2020-01', '2020-02': '2020-02', . . . . . .}
    """
    years = ['2020','2021','2022','2023'] # should add more years ?
    periods = {}
    for y in years:
        for m in range(1,13):
            # full_month = calendar.month_name[m] # for complete month name
            # abbr_month = calendar.month_abbr[m]
            # period = abbr_month + '-' + y

            m = str.zfill( str(m), 2) # when 1 digit, then add a 0 before the digit

            period = y + '-' + m

            d = {period: period } 
            periods.update(d)

    return periods


# if user change period format then these functions will need be refactored
def get_first_day( period ):
    y = period.split('-')[0]
    m = period.split('-')[-1]
    date = datetime.date( int(y), int(m), 1)
    """ Create date object in given time format mm/dd/yyyy """
    # date = datetime.strptime(period, "%m/%d/%Y") 
    # first = date.replace(day = 1)
    first_str = date.strftime( OUTPUT_DATE_FORMAT ) 
    return first_str


def get_last_day( period ):
    y = period.split('-')[0]
    m = period.split('-')[-1]
    date = datetime.date( int(y), int(m), 1)
    """ Create date object in given time format mm/dd/yyyy """
    # date = datetime.strptime(period, "%m/%d/%Y") 
    """ replace the day number with the total number of days in that month."""
    last = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    last_str = last.strftime( OUTPUT_DATE_FORMAT ) 
    return last_str


def get_internal_period_number( period, periods ):
    """ TODO : change this. user should only have to specify which period is 1. something similar to how is done above

        for some reason, peachtree have an internal period number that depends of when when the client was first created in peachtree. & it has to be in each transaction csv line.  Do other accounting software also have this ?
    """

    if period == periods['2021-01']: return '1'
    if period == periods['2021-02']: return '2'
    if period == periods['2021-03']: return '3'
    if period == periods['2021-04']: return '4'
    if period == periods['2021-05']: return '5'
    if period == periods['2021-06']: return '6'
    if period == periods['2021-07']: return '7'
    if period == periods['2021-08']: return '8'
    if period == periods['2021-09']: return '9'
    if period == periods['2021-10']: return '10'
    if period == periods['2021-11']: return '11'
    if period == periods['2021-12']: return '12'

    if period == periods['2022-01']: return '13'
    if period == periods['2022-02']: return '14'
    if period == periods['2022-03']: return '15'
    if period == periods['2022-04']: return '16'
    if period == periods['2022-05']: return '17'
    if period == periods['2022-06']: return '18'
    if period == periods['2022-07']: return '19'
    if period == periods['2022-08']: return '20'
    if period == periods['2022-09']: return '21'
    if period == periods['2022-10']: return '22'
    if period == periods['2022-11']: return '23'
    if period == periods['2022-12']: return '24'

    print('== == ==> Internal period number not found for Client & Period. See get_internal_period() in client functions periods.py ')
    exit()

