from datetime import datetime

def get_last_month_period():
    today = datetime.today()
    month = today.month
    last_month =  str( month - 1 if month > 1 else 12 )
    last_month = '0' + last_month if len(last_month) == 1 else last_month
    year = str( today.year if month > 1 else today.year -1 )
    return year + "-" + last_month