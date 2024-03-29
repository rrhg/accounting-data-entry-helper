import time
from utils.csv2.create_output_csv_file import create_debits_csv_file
from transactions.compare_sums_of_transactions import compare_sums_of_debits
from transactions.get_all import get_all_debits
from config import model, client, STATEMENT_PDF

# import typer
# app = typer.Typer()

# @app.command()
# def debits(model_logs: str = False):
def debits():

    all_debits = get_all_debits()

    # print(all_debits)

    compare_sums_of_debits( all_debits )

    create_debits_csv_file( all_debits )

    model.save_model()

if __name__ == '__main__':
    # app()
    debits()
