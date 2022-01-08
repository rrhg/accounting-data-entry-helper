import json
import sys
from os.path import join
from pathlib import Path
from utils.prompt_user_autocomplete import prompt_user_autocomplete
from utils.files import create_dir_w_parents, get_clients_names_from_dir
from utils.json import get_dict_from_json_file



PATH_FOR_PROJECT = Path(__file__).parent.parent

clients_folder = 'accounting_clients'

PATH_FOR_CLIENTS = create_dir_w_parents( join(PATH_FOR_PROJECT, clients_folder )  )

clients = get_clients_names_from_dir(PATH_FOR_CLIENTS)
""" clients == our accounting clients; customers==customers to our clients; definition of client == seek professional services, longer business relashionship """


# current client
client_name = prompt_user_autocomplete( 'Select a client : ', clients )
imported_client_module = getattr(__import__( clients_folder , fromlist=[ client_name ]), client_name )
""" is equivalent to: from accounting_clients import <client_name> as imported_client_module """
client = imported_client_module.client

PATH_THIS_CLIENT = create_dir_w_parents( join(PATH_FOR_CLIENTS, client_name )  )

STATEMENT_DATA_FILE = client.get_txt_input_file_path()
STATEMENT_PDF = client.get_pdf_statement_file_path()



# periods
periods = client.get_periods()
PERIOD = prompt_user_autocomplete( 'Select a period : ', periods.keys() )
INTERNAL_PERIOD_NUMBER = client.get_internal_period_number( PERIOD, periods )
DATE_END_OF_PERIOD = client.get_last_day( PERIOD )
DATE_BEG_OF_PERIOD = client.get_first_day( PERIOD )

VENDOR_CREATED_DATE = DATE_BEG_OF_PERIOD
DATE_FOR_TRANSACTIONS = DATE_END_OF_PERIOD
YEAR_FOR_DATE = DATE_END_OF_PERIOD.split('/')[-1]



# BANK_ACCOUNT = client.get_bank_account() # TODO delete ?



# output
PATH_FOR_OUTPUT = client.get_folder_path_for_output()
if not PATH_FOR_OUTPUT:
    PATH_FOR_OUTPUT = create_dir_w_parents( join( PATH_THIS_CLIENT, 'output')  )

PATH_FOR_PERIOD = create_dir_w_parents( join( PATH_FOR_OUTPUT, PERIOD)  )
OUTPUT_CSV_FILE_FOR_CREDITS = join(PATH_FOR_PERIOD, 'credits.csv')
OUTPUT_CSV_FILE_FOR_DEBITS =  join(PATH_FOR_PERIOD, 'debits.csv')
OUTPUT_CSV_FILE_FOR_NEW_VENDORS =  join(PATH_FOR_PERIOD, 'vendors.csv')
OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS =  join(PATH_FOR_PERIOD, 'customers.csv')



# client_partners ( vendors & customers )
PATH_CLIENT_PARTNERS = create_dir_w_parents( join(PATH_THIS_CLIENT , 'partners')  )
PATH_FOR_PARTNERS_DATA_BACKUP = create_dir_w_parents( join(PATH_CLIENT_PARTNERS,'backup')  )

VENDORS_JSON_FILE_NAME = 'all_vendors.json'
VENDORS_JSON_FILE = join(PATH_CLIENT_PARTNERS, VENDORS_JSON_FILE_NAME)
VENDORS_JSON_BACKUP_FILE = join(PATH_FOR_PARTNERS_DATA_BACKUP, VENDORS_JSON_FILE_NAME)

CUSTOMERS_JSON_FILE_NAME = 'all_customers.json'
CUSTOMERS_JSON_FILE = join(PATH_CLIENT_PARTNERS, CUSTOMERS_JSON_FILE_NAME)
CUSTOMERS_JSON_BACKUP_FILE = join(PATH_FOR_PARTNERS_DATA_BACKUP, CUSTOMERS_JSON_FILE_NAME)

# TODO research why 2 customers files?? to delete ??
PATH_CUSTOMERS = create_dir_w_parents( join(PATH_THIS_CLIENT , 'customers')  )
CUSTOMERS_FILE = join( PATH_CUSTOMERS, 'customers.json' )

CUSTOMERS = get_dict_from_json_file(CUSTOMERS_FILE) # TODO delete ??

VENDOR_CSV_WAS_CREATED = False # TODO delete ?
# always delete from previous run
DELETE_PREVIOUS_VENDOR_CSV_FILE = True # TODO delete ?



# --- original csv files exported from peachtree
# TODO: change 'original_peachtree_csv_files' to 'original_csv_files'
# ORIGINAL_CSV_FILES_FOLDER = join(PATH_FOR_PROJECT, 'original files')
ORIGINAL_CSV_FILES_FOLDER = join(PATH_THIS_CLIENT, 'original_peachtree_csv_files')
ORIGINAL_FILES_PAYMENTS = join(ORIGINAL_CSV_FILES_FOLDER, 'PAYMENTS.csv')
ORIGINAL_FILES_RECEIPTS = join(ORIGINAL_CSV_FILES_FOLDER, 'RECEIPTS.csv')
ORIGINAL_CSV_FILE_VENDORS = join(ORIGINAL_CSV_FILES_FOLDER, 'VENDOR.csv')
ORIGINAL_CSV_FILE_CUSTOMERS = join(ORIGINAL_CSV_FILES_FOLDER, 'CUSTOMER.csv')



# entered checks
ENTERED_CHECKS_FOLDER = create_dir_w_parents(   join( PATH_FOR_PERIOD, 'entered_checks' )   )
ENTERED_CHECKS_FILE = join( ENTERED_CHECKS_FOLDER, 'entered_checks.json' )



# ignored lines
PATH_IGNORED_LINES = join( PATH_THIS_CLIENT, 'ignored_lines' )
IGNORED_DEBIT_LINES_FILE = join( PATH_IGNORED_LINES, 'ignored_debit_lines.json' )
IGNORED_CREDIT_LINES_FILE = join( PATH_IGNORED_LINES, 'ignored_credit_lines.json' )


# other variables
REFERENCE_FOR_DEBITS_THAT_ARE_NOT_CHECKS = 'Debit'

debit = 'debit'
credit = 'credit'
vendor = 'vendor'
customer = 'customer'

partner_code = 'code'
partner_name = 'name'
partner_account = 'account'
partner_description = 'description'
partner_memo = 'memo'
partner_strings = 'strings'