# from config import ENTERED_CHECKS_FILE
from utils.json import get_dict_from_json_file
from utils.json import write_dict_to_json_file
from .create_if_no_entered_cks_file import create_if_no_entered_cks_file


def add_to_entered_checks( vendor_dict_with_ck_info, file ):

    create_if_no_entered_cks_file( file )

    dict_of_dicts = get_dict_from_json_file( file )

    dict_to_save = { # ck number will be the key for each dict
        vendor_dict_with_ck_info['ck_number']: vendor_dict_with_ck_info
    }

    dict_of_dicts.update( dict_to_save )
    # print( dict_of_dicts )
    """
    TODO : TypeError: 'module' object is not callable. Is bc this functions expect letters(not numbers) in the keys bc is trying to convert it to lower case. Should it be fix to order this file by check number ?? 
    # from utils.vendors import new_ordered_dict_by_key_string # now I think is in client_partners
    ordered = new_ordered_dict_by_key_string( dict_of_dicts )
    write_dict_to_json_file(ordered, file)
    """
    write_dict_to_json_file( dict_of_dicts, file)