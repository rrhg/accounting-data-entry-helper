from config import (
    OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS,
    OUTPUT_CSV_FILE_FOR_NEW_VENDORS,
    ORIGINAL_CSV_FILE_VENDORS,
    VENDOR_CREATED_DATE,
    vendor,
    customer
)


""" 
    TODO now, not sure in what scenario will this be useful.
    Can this file be deleted ? 
"""

def should_we_delete_previous_partners_in_file( vendor_dict, ptype=vendor ):

    out_file = OUTPUT_CSV_FILE_FOR_NEW_VENDORS
    if ptype == customer:
        out_file = OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS

    def clear_previous_vendors_csv_file():
        f = open(out_file, '+w')
        f.close()

    while True:
        a = input('Should we clear previous csv file with NEW '+ ptype +'s  ? ')
        if a == 'y' or a == 'Y':
            clear_previous_vendors_csv_file()
            break
        if a == 'n' or a == 'N':
            break