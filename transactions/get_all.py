from config import debit, credit, STATEMENT_DATA_FILE, client, STATEMENT_PDF
import config
from utils import lines
from .convert_lines_into_transactions import convert_lines_into_transactions
from .extract_section_lines import extract_section_lines
from .ignored_lines import remove_ignored_lines
from utils.pdf.pdf2txt import extract_lines_of_txt_from_searchable_pdf

def get_all(statement_text_file, trans_type=debit):

    # not working bc PyPDF2, pypdfminer & other packages, non were 100% reliable. Some lines were missing. Maybe the PDFs I received, even thou some of them are text searchable, aparently have some probems, as clients tend to use the print_to_pdf function in windows 10.
    # if hasattr(client, 'statement_is_searchable_pdf'):
    #     print(f"extracting text from {STATEMENT_PDF}")
    #     all_lines = extract_lines_of_txt_from_searchable_pdf(STATEMENT_PDF)
    # else:
    #     all_lines = lines.decode_lines( statement_text_file )
    
    if hasattr(client, 'get_transactions_and_convert_pdf2txt_in_1_step'):
        from utils.pdf.pdf2txt import pdf2txt
        pdf2txt()

    all_lines = lines.decode_lines( statement_text_file )

    # for l in all_lines:
    #     print(l)
    # import sys
    # sys.exit(0)


    """ important: do not remove ignored lines here, in case user has added 1st & last line of debits to ignored lines """
    lines_btn_1st_and_last = extract_section_lines( all_lines, trans_type=trans_type )
    

    # Testing if is better to:
    #    not remove lines here
    #    instead ignore them in convert_non_ck_lines_into_transactions
    #    because some ignored lines are used as previous lines
    # """ now we can remove ignored lines"""
    # all_lines = remove_ignored_lines( all_lines, trans_type=trans_type )
    # lines_btn_1st_and_last = remove_ignored_lines( lines_btn_1st_and_last, trans_type=trans_type )
    

    transactions = convert_lines_into_transactions( all_lines, lines_btn_1st_and_last, trans_type=trans_type )
    
    if hasattr(client, 'create_reconciliation_file'):
        client.create_reconciliation_file(transactions, config, all_lines)

    """ transactions is a list of dicts"""
    return transactions


def get_all_debits():
    return get_all(STATEMENT_DATA_FILE, trans_type=debit)


def get_all_credits():
    return get_all(STATEMENT_DATA_FILE, trans_type=credit)
