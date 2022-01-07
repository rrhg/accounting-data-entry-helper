import csv
from config import (
    OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS,
    OUTPUT_CSV_FILE_FOR_NEW_VENDORS,
    ORIGINAL_CSV_FILE_VENDORS,
    ORIGINAL_CSV_FILE_CUSTOMERS,
    VENDOR_CREATED_DATE,
    vendor,
    customer
)
from .get_one_csv_row_from_file import get_one_csv_row_from_file


def add_partner_to_csv_file( partner_dict, ptype=vendor ):
    out_file = OUTPUT_CSV_FILE_FOR_NEW_VENDORS
    original_csv_file = ORIGINAL_CSV_FILE_VENDORS
    if ptype == customer:
        out_file = OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS
        original_csv_file = ORIGINAL_CSV_FILE_CUSTOMERS

    
    # TODO  this should be in client_name / functions / csv
    #       use columns headers & pandas dataframe ??
    csv_row = get_one_csv_row_from_file(original_csv_file) 

    # TODO THIS IS WHAT NEEDS TO BE SOMEHOW EDITED BY USER IN A FUNCTION FOR EACH CLIENT
    if ptype == vendor:
        csv_row[0] = partner_dict['code']
        csv_row[1] = partner_dict['name']
        csv_row[11] = partner_dict['type']
        csv_row[17] = partner_dict['account']
        csv_row[19] = partner_dict['memo']
        csv_row[33] = VENDOR_CREATED_DATE

    if ptype == customer:
        csv_row[0] = partner_dict['code']
        csv_row[1] = partner_dict['name']
        # csv_row[11] = partner_dict['type']
        csv_row[27] = partner_dict['account']
        # csv_row[19] = partner_dict['memo']
        csv_row[59] = VENDOR_CREATED_DATE

    # with open(output_file, 'w') as f:
    """ before this, it was adding an empty line between csv lines # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows """
    with open(out_file, 'a', newline='\n', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        # w = csv.writer(f)
        # w.writerows(csv_rows)
        w.writerow(csv_row)