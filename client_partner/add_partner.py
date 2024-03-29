from config import vendor, customer
from .get_all import get_all
from .write_dict_to_json_file import write_dict_to_json_file
from .make_bakup import make_bakup
from .new_ordered_dict_by_key_string import new_ordered_dict_by_key_string
from utils.csv2 import add_partner_to_csv_file
from config import VENDORS_JSON_FILE, CUSTOMERS_JSON_FILE

"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""

def add_partner(partner_dict, ptype=vendor):
    add_partner_to_csv_file(partner_dict, ptype=ptype) # output for importing in accounting software
    add_to_json_file(partner_dict, ptype=ptype) # to update file with all partners(do we need a database?) 


def add_to_json_file(partner_dict, ptype=vendor):    
    # TODO fix partner_dict. Should it be a class. ?
    new = { 
        partner_dict['code']: {
            "code":                 partner_dict['code'],
            "name":                 partner_dict['name'],
            "account":              partner_dict['account'],
            "account_can_change":    partner_dict['account_can_change'],
            "description":          partner_dict['memo'],
            "affects_more_than_1_account":    partner_dict['affects_more_than_1_account'],
            "accounts":             partner_dict['accounts'],
            "split_amount_in_half": partner_dict['split_amount_in_half'],
            "strings":              partner_dict['strings'], # list of lists
        }}

    pfile = VENDORS_JSON_FILE
    if ptype == customer:
        pfile = CUSTOMERS_JSON_FILE
    
    make_bakup(pfile)

    partners = get_all( ptype=ptype )
    partners.update( new )
    ordered = new_ordered_dict_by_key_string( partners )
    write_dict_to_json_file( ordered, pfile )
