# from config import ENTERED_CHECKS_FILE
from utils.json import get_dict_from_json_file
from utils.json import write_dict_to_json_file
from .create_if_no_entered_cks_file import create_if_no_entered_cks_file


def ck_was_already_entered( ck_number, ENTERED_CHECKS_FILE ):

    create_if_no_entered_cks_file( ENTERED_CHECKS_FILE )

    dict_of_dicts = get_dict_from_json_file( ENTERED_CHECKS_FILE )

    for entered_ck_number in dict_of_dicts.keys():
        if ck_number == entered_ck_number:
            return True
            # print(ck_number + ' was alreadyentered')

    return False