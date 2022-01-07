from config import client, debit, credit
from .convert_checks_lines_into_transactions import convert_checks_lines_into_transactions
from .search_and_add_transactions_from_bank_charges import search_and_add_transactions_from_bank_charges
from .convert_non_ck_lines_into_transactions import convert_non_ck_lines_into_transactions
from .convert_credit_lines_into_transactions import convert_credit_lines_into_transactions
from .extract_cks_lines import extract_cks_lines


def convert_lines_into_transactions( all_lines, found_lines, trans_type=debit ):

    """ transactions is a list of dicts"""
    transactions = []

    # TODO : maybe this should be 1 function convert_debit_lines... & should be in another file
    if trans_type == debit:
        """ do this first in case can not find bank charges, script will ask if user wants to continue """
        if client.there_are_additional_bank_charges_outside_debits_lines():
            not_found_lines = [l for l in all_lines if l not in found_lines]
            search_and_add_transactions_from_bank_charges( not_found_lines, transactions )

        checks_lines, non_ck_debit_lines = extract_cks_lines(found_lines)

        convert_checks_lines_into_transactions( checks_lines, transactions )

        convert_non_ck_lines_into_transactions( non_ck_debit_lines, transactions )

    if trans_type == credit:
        convert_credit_lines_into_transactions( found_lines, transactions )

    return transactions
