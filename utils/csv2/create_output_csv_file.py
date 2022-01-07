from config import ( client, debit, credit, vendor, customer,
                     OUTPUT_CSV_FILE_FOR_NEW_VENDORS, OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS,
                    OUTPUT_CSV_FILE_FOR_DEBITS, OUTPUT_CSV_FILE_FOR_CREDITS )
from .write_rows_to_csv_file import write_rows_to_csv_file


def create_debits_csv_file( all_transactions ):
    create_output_csv_file( all_transactions, transactions_type=debit, ptype=vendor )

def create_credits_csv_file( all_transactions ):
    create_output_csv_file( all_transactions, transactions_type=credit, ptype=customer )


def create_output_csv_file( all_transactions, transactions_type=debit, ptype=vendor ):
    output_file = OUTPUT_CSV_FILE_FOR_DEBITS
    new_partners_file = OUTPUT_CSV_FILE_FOR_NEW_VENDORS
    transaction_to_csv_row = client.debit_transaction_to_csv_row
    if transactions_type == credit:
        output_file = OUTPUT_CSV_FILE_FOR_CREDITS
        new_partners_file = OUTPUT_CSV_FILE_FOR_NEW_CUSTOMERS
        transaction_to_csv_row = client.credit_transaction_to_csv_row

    csv_rows = []

    for index, transaction in enumerate(all_transactions):

        """  this one have to be done here """
        transaction.transaction_number = index + 1

        row = transaction_to_csv_row( transaction )
        csv_rows.append( row )
    
    write_rows_to_csv_file(output_file, csv_rows)
    
    print()
    print("DONE! Transactions data is in ==> ", output_file)
    print()
    print()
    print('New partners data is in ==> ', new_partners_file )
    print()



