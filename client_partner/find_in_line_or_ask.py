from config import client, vendor, customer
from utils.lines import whole_line_is_a_key 
from .find_strings_in_line import find_strings_in_line
from .get_all import get_all
from .ask_to_create_partner_or_ignore_line import ask_to_create_partner_or_ignore_line


def find_in_line_or_ask(line,
                        previous_line,
                        ptype=vendor,
                        is_check=False,
                        infered_payee_in_ck_image="",
                        msg_if_not_found=''):

    partners_dict = get_all(ptype=ptype) # vendor will get all vendors & custmer will get all customers from json file
    partner_key = find_strings_in_line(line,
                                       previous_line,
                                       partners_dict,
                                       is_check=is_check,
                                       infered_payee_in_ck_image=infered_payee_in_ck_image
                                       )
    if partner_key:
        return partner_key

    # not anymore. now checks r done similar to non cks but with infered payee
    # if ptype == vendor and client.is_a_line_of_checks( line, previous_line):
    #     partner_key = 'is_a_check'
    #     return partner_key
 
    """ ask - bc did not found """
    partner_key = ask_to_create_partner_or_ignore_line(line, previous_line, ptype=ptype, msg_if_not_found=msg_if_not_found)
    if partner_key:
        return partner_key
        
    return False


def find_vendor_in_line_or_ask(line, previous_line, is_check=False, infered_payee_in_ck_image="", msg_if_not_found=''):
    return find_in_line_or_ask(line, previous_line, ptype=vendor,is_check=is_check, infered_payee_in_ck_image=infered_payee_in_ck_image, msg_if_not_found=msg_if_not_found )

def find_customer_in_line_or_ask(line, previous_line, msg_if_not_found=''):
    return find_in_line_or_ask(line, previous_line, ptype=customer, msg_if_not_found=msg_if_not_found )
