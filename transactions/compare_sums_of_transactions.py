from config import client, debit, credit, STATEMENT_DATA_FILE
from utils.strings import try_convert_amount_to_float
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")

def compare_sums_of_debits(processed_transactions):
    compare_sums_of_transactions(processed_transactions, STATEMENT_DATA_FILE, trans_type=debit)

def compare_sums_of_credits(processed_transactions):
    compare_sums_of_transactions(processed_transactions, STATEMENT_DATA_FILE, trans_type=credit)


def compare_sums_of_transactions(processed_transactions, statement_data_file, trans_type=debit):

    # print('processed_transactions ==> ', processed_transactions)

    print("====================================")
    print(f"  Now comparing totals")
    print(f"     Reminder: a problem here could be in client functions get_debits_total_from_statement. (En Vida lo arregle por la cantidad)\n")

    def get_total_after_processing(processed_transactions):
        total = 0
        for t in processed_transactions:
            if type(t) is dict:
                print('try to comvert amount of a dict. dict ==> ')
                print(t)
                print()
            amount = try_convert_amount_to_float( t.amount, t )
            # print('amount ==> ', amount)
            # print('amount type ==> ', type(amount) )
            # print(t)
            total += amount 
        return round( total ,2 )

    after_processing = get_total_after_processing(processed_transactions)

    from_statement = 0
    if trans_type == debit:
        from_statement = client.get_debits_total_from_statement(statement_data_file)
    if trans_type == credit:
        from_statement = client.get_credits_total_from_statement(statement_data_file)

    if from_statement != after_processing:
        red.print('TRANSACTIONS TOTAL IS  NOT  BALANCED. !!!!!!!!!')
        red.print(" One way to fix can be to go to the resulrs.txt (data extracted from the bank statement pdf) & correct it. Maybe data was not read correctly bc it first converted to an image (jpeg)")
    else:
        red.print("TRANSACTIONS TOTAL IS BALANCED. DATA WAS READ CORRECTLY")
    print(" ==> in statement", from_statement)
    print(" ==> after read data", after_processing)
    diff = from_statement - after_processing
    print(" diff ============>>>>>>> ", diff)
    print("============================================================")



