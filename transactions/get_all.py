from config import debit, credit, STATEMENT_DATA_FILE
from utils import lines
from .convert_lines_into_transactions import convert_lines_into_transactions
from .extract_section_lines import extract_section_lines
from .ignored_lines import remove_ignored_lines


def get_all(statement_text_file, trans_type=debit):

    all_lines = lines.decode_lines( statement_text_file )

    """ important: do not remove ignored lines here, in case user has added 1st & last line of debits to ignored lines """
    lines_btn_1st_and_last = extract_section_lines( all_lines, trans_type=trans_type )

    """ now we can remove ignored lines"""
    all_lines = remove_ignored_lines( all_lines, trans_type=trans_type )
    lines_btn_1st_and_last = remove_ignored_lines( lines_btn_1st_and_last, trans_type=trans_type )

    transactions = convert_lines_into_transactions( all_lines, lines_btn_1st_and_last, trans_type=trans_type )
    
    """ transactions is a list of dicts"""
    return transactions


def get_all_debits():
    return get_all(STATEMENT_DATA_FILE, trans_type=debit)


def get_all_credits():
    return get_all(STATEMENT_DATA_FILE, trans_type=credit)
