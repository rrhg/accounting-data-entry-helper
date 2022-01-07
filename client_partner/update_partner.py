from .get_all import get_all
from config import vendor, customer, partner_code, partner_name, partner_account, partner_description, partner_memo, partner_strings
from config import VENDORS_JSON_FILE, CUSTOMERS_JSON_FILE
from .make_bakup import make_bakup
from .write_dict_to_json_file import write_dict_to_json_file



def update_partner( partner_key, account='', strings_list='', ptype=vendor, utype=partner_strings):
    """ Update partner in json file. Useful when it was already updated in the accounting software or when we want to add a list of strings to search for this partner in a aline """
    # TODO this can be used to also update account & other partner attributes
    partners = get_all( ptype=ptype ) # get a new one in case it has new vendors or customers
    partner = partners[partner_key]

    if utype == partner_strings:
        partner[partner_strings].append( strings_list)

    pfile = VENDORS_JSON_FILE
    if ptype == customer:
        pfile = CUSTOMERS_JSON_FILE
    
    make_bakup(pfile)

    # may not be needed partners.update( new )
    # may or may not needed ordered = new_ordered_dict_by_key_string( partners )
    write_dict_to_json_file( partners, pfile )
