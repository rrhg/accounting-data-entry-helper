from pathlib import Path
from os.path import join
import os

"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""

PATH_FOR_CLIENT = Path(__file__).parent.parent

BANK_STATEMENT_DIR = join(PATH_FOR_CLIENT, "bank_statement")
if not os.path.exists(BANK_STATEMENT_DIR):
    os.makedirs(BANK_STATEMENT_DIR)


def get_folder_path_for_output():
    # return False # if False, all output will be in accountant_helper/accounting_clients/<client name>/output
    # return r"C:\Users\full\path\to\output\folder" # if u want output(debits/credits csv files) in another directory
    output_dir = join(PATH_FOR_CLIENT, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


#TODO rename to statement_txt_file():
def get_txt_input_file_path():
    """ text file after pdf statement was converted to txt. Or csv statement was converted to txt"""
    #return r'C:/Users/full/path/to/file.txt' # if not using pdf2txt.py . For example, using a statement that is already in a txt file
    filepath = join(BANK_STATEMENT_DIR, "bank_statement.txt")
    return filepath


def get_pdf_statement_file_path():
    """  pdf bank statement to be used by pdf2txt.py(Tesseract) to be converted to text"""
    # return join(BANK_STATEMENT_DIR, 'file name goes here.pdf') # if you saves statement pdf to \accounting_clients\<name>\bank_statement\
    return r'C:/Users/full/path/to/file.pdf'


def file_with_new_customers_to_import():
    return False # try to always return False when not importing, to avoid errors
    # return r'C:\Users\full\path\to\file.csv'


def file_with_new_vendors_to_import():
    return False # try to always return False when not importing, to avoid errors
    # return r'C:\Users\full\path\to\file.csv'
