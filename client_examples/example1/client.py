from pathlib import Path


# TODO change. just import eveything ??
class client:
    name = Path(__file__).parent.name # parent_folder_name

    from .functions.files import get_txt_input_file_path, file_with_new_vendors_to_import, file_with_new_customers_to_import, get_folder_path_for_output, get_pdf_statement_file_path
    get_pdf_statement_file_path = get_pdf_statement_file_path
    get_folder_path_for_output = get_folder_path_for_output
    file_with_new_customers_to_import = file_with_new_customers_to_import
    file_with_new_vendors_to_import = file_with_new_vendors_to_import
    get_txt_input_file_path = get_txt_input_file_path


    from .functions.compare_totals import get_credits_total_from_statement, get_debits_total_from_statement
    get_credits_total_from_statement = get_credits_total_from_statement
    get_debits_total_from_statement = get_debits_total_from_statement


    from .functions.get_bank_account import get_bank_account
    get_bank_account = get_bank_account

    
    from .functions.debits_lines import date_is_in_previous_debit_line, get_date_str_from_debit_line, get_amount_str_from_debit_line, is_not_a_debit_line, is_1st_line_of_debits, is_last_line_of_debits, do_nothing_but_keep_debit_line, amount_is_in_previous_debit_line
    get_amount_str_from_debit_line = get_amount_str_from_debit_line
    get_date_str_from_debit_line = get_date_str_from_debit_line
    is_not_a_debit_line = is_not_a_debit_line
    is_1st_line_of_debits = is_1st_line_of_debits
    is_last_line_of_debits = is_last_line_of_debits
    do_nothing_but_keep_debit_line = do_nothing_but_keep_debit_line
    amount_is_in_previous_debit_line = amount_is_in_previous_debit_line
    date_is_in_previous_debit_line = date_is_in_previous_debit_line


    from .functions.credits_lines import date_is_in_previous_credit_line, get_date_str_from_credit_line, get_amount_str_from_credit_line, is_not_a_credit_line, is_1st_line_of_credits, is_last_line_of_credits, do_nothing_but_keep_credit_line, amount_is_in_previous_credit_line
    get_date_str_from_credit_line = get_date_str_from_credit_line
    get_amount_str_from_credit_line = get_amount_str_from_credit_line
    is_not_a_credit_line = is_not_a_credit_line
    is_1st_line_of_credits = is_1st_line_of_credits
    is_last_line_of_credits = is_last_line_of_credits
    do_nothing_but_keep_credit_line = do_nothing_but_keep_credit_line
    amount_is_in_previous_credit_line = amount_is_in_previous_credit_line
    date_is_in_previous_credit_line = date_is_in_previous_credit_line
    

    from .functions.bank_charges import there_are_additional_bank_charges_outside_debits_lines, line_contains_bank_charges
    there_are_additional_bank_charges_outside_debits_lines = there_are_additional_bank_charges_outside_debits_lines
    line_contains_bank_charges = line_contains_bank_charges



    from .functions.checks_lines import is_a_line_of_checks, get_amount_str_from_ck_line, get_date_from_ck_line, get_ck_number_from_ck_line, get_1st_ck_line_from_line, get_2nd_ck_line_from_line, line_has_more_than_1_ck, clean_ck_line
    is_a_line_of_checks = is_a_line_of_checks
    get_amount_str_from_ck_line = get_amount_str_from_ck_line
    get_date_from_ck_line = get_date_from_ck_line
    get_ck_number_from_ck_line = get_ck_number_from_ck_line
    line_has_more_than_1_ck = line_has_more_than_1_ck
    clean_ck_line = clean_ck_line
    get_1st_ck_line_from_line = get_1st_ck_line_from_line
    get_2nd_ck_line_from_line = get_2nd_ck_line_from_line


    from .functions.periods import get_periods, get_internal_period_number, get_first_day, get_last_day
    get_periods = get_periods
    get_internal_period_number = get_internal_period_number
    get_first_day = get_first_day
    get_last_day = get_last_day

    from .functions.csv import convert_imported_vendor_csv_row_to_dict, credit_transaction_to_csv_row, debit_transaction_to_csv_row, convert_imported_customer_csv_row_to_dict
    convert_imported_vendor_csv_row_to_dict = convert_imported_vendor_csv_row_to_dict
    convert_imported_customer_csv_row_to_dict = convert_imported_customer_csv_row_to_dict 
    debit_transaction_to_csv_row =              debit_transaction_to_csv_row
    credit_transaction_to_csv_row =             credit_transaction_to_csv_row
    
    
    from .functions.transactions import use_end_of_period_for_all_trans_w_date_errors
    use_end_of_period_for_all_trans_w_date_errors = use_end_of_period_for_all_trans_w_date_errors