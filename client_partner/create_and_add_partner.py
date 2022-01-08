from config import vendor, customer
from .get_partner_info_from_user import get_partner_info_from_user
from .add_partner import add_partner

"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""

def create_and_add_partner(line, previous_line, ptype=vendor ):

    # vendor_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
    partner_dict = get_partner_info_from_user( ptype=ptype )

    add_partner( partner_dict, ptype=ptype ) # to both: csv & json # imported from vendors

    return partner_dict