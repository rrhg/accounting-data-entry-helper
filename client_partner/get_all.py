from utils.json import get_dict_from_json_file
from config import (
    customer,
    vendor, 
    VENDORS_JSON_FILE,
    CUSTOMERS_JSON_FILE
)

"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""

def get_all(ptype=vendor):
    """ returns a dict of all partners """
    if ptype == vendor:
        d = get_dict_from_json_file( VENDORS_JSON_FILE ) # will create file if not exist
    if ptype == customer:
        d = get_dict_from_json_file( CUSTOMERS_JSON_FILE )
    return d