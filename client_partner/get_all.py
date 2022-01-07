from utils.json import get_dict_from_json_file
from config import (
    customer,
    vendor, 
    VENDORS_JSON_FILE,
    CUSTOMERS_JSON_FILE
)


def get_all(ptype=vendor):
    """ returns a dict"""
    if ptype == vendor:
        d = get_dict_from_json_file( VENDORS_JSON_FILE ) # will create file if not exist
    if ptype == customer:
        d = get_dict_from_json_file( CUSTOMERS_JSON_FILE )
    return d