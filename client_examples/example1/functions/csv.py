import csv

"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""


# TODO: comment with better explanation 
def convert_imported_customer_csv_row_to_dict( csv_row, partner_dict ):
    """ This function is only used when importing customers from csv file. For example: 1- you created a new client here using new_client.py. 2- exported the client customers from the accounting software to a csv file. 3- added the file w full path to clien/functions/files.file_with_new_customers_to_import(). 4- import customers here with import_customers.py """
    c = partner_dict.copy()
    """ csv_row has already been converted to a list """
    c['code'] = csv_row[0]
    c['name'] = csv_row[1]
    c['account'] = csv_row[27]
    c['strings'] = [ csv_row[0].split(), csv_row[1].split() ]
    """ Withoug making a dict copy, doesn't work """
    dict_copy = c.copy()
    return dict_copy


def convert_imported_vendor_csv_row_to_dict( csv_row, partner_dict ):
    """ This function is only used when importing vendors from csv file. For example: 1- you created a new client here using new_client.py. 2- exported the client vendors from the accounting software to a csv file. 3- added the file w full path to clien/functions/files.file_with_new_vendors_to_import(). 4- import vendors here with import_vendors.py """
    c = partner_dict.copy()
    """ csv_row has already been converted to a list """
    c['code'] = csv_row[0]
    c['name'] = csv_row[1]
    c['account'] = csv_row[27]
    c['strings'] = [ csv_row[0].split(), csv_row[1].split() ]
    """ Withoug making a dict copy, doesn't work """
    dict_copy = c.copy()
    return dict_copy


def credit_transaction_to_csv_row(transaction):
    """ Customize csv rows in the (output)credits.csv file to be imported in your accounting software """
    number_of_row_items = 45 # 45 items in a csv row in the old peachtree file named RECEIPTS.csv 
    row = ['' for n in range( number_of_row_items )]
    # info about fields:  https://help-sage50.na.sage.com/en-us/2019/Content/Importing_Exporting/Import_Export_Fields/Import_Export_Field_Definition_Lists.htm   https://help-sage50.na.sage.com/en-us/2019/Content/Importing_Exporting/Import_Export_Fields/IEFIELDS_Cash_Disbursements_Journal.htm
    t = transaction
    row[1] = t.partner_code
    row[2] = t.partner_name
    row[3] = 'Deposits' # Reference
    row[4] = t.date
    row[5] = 'Check' # Payment Method
    row[6] = t.bank_account # bank account
    row[7] = '1' # it was '286' # don't know. Appears to be some kind of cash balance used only during exporting ?
    row[10] = '0' # ?
    row[12] = 'FALSE'
    row[13] = 'FALSE'
    row[14] = t.date
    row[15] = '1' # Number of distributions ? (could it be # transactions in a single deposit ? )
    row[17] = '0' # ?
    row[18] = '0' # ?
    row[20] = t.date
    row[21] = t.account
    row[22] = '0' # ?
    row[23] = '1' # ?
    row[25] = '0' # ?
    row[26] = '-' + t.amount # amount here has to be negative
    row[29] = t.internal_period_number
    row[30] = t.transaction_number
    row[42] = '0' # ?
    row[44] = '0' # ?
    # row[9] = t.ck_number
    # row[15] = t.memo
    return row


def debit_transaction_to_csv_row(transaction):
    """ Customize csv rows in the (output)debits.csv file to be imported in your accounting software """

    number_of_row_items = 41 # number of items in old peachtree csv file PAYMENTS.csv 
    row = ['' for n in range( number_of_row_items )]
    # info about fields:  https://help-sage50.na.sage.com/en-us/2019/Content/Importing_Exporting/Import_Export_Fields/Import_Export_Field_Definition_Lists.htm   https://help-sage50.na.sage.com/en-us/2019/Content/Importing_Exporting/Import_Export_Fields/IEFIELDS_Cash_Disbursements_Journal.htm
    t = transaction
    row[0] = t.partner_code
    row[1] = t.partner_name
    row[2] = t.partner_name
    row[9] = t.ck_number
    row[10] = t.date # now we are converting line when getting transaction info from line
    row[11] = 'FALSE'
    row[15] = t.memo
    row[16] = t.bank_account
    row[17] = '0'
    row[19] = 'FALSE'
    row[20] = 'FALSE'
    row[21] = t.date
    row[22] = 'Yes'
    row[23] = '1'
    row[25] = '0'
    row[26] = '0'
    row[29] = t.account
    row[30] = '0'
    row[32] = '0'
    row[33] = t.amount
    row[35] = 'FALSE'
    row[36] = t.internal_period_number
    row[37] = t.transaction_number
    row[39] = '0'
    row[40] = '0'
    return row