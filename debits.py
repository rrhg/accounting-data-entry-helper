import typer
from utils.csv2.create_output_csv_file import create_debits_csv_file
from transactions.compare_sums_of_transactions import compare_sums_of_debits
from transactions.get_all import get_all_debits
from config import model

app = typer.Typer()

@app.command()
def debits(model_logs: str = False):
    # cli argument use: python debits.py --model-logs true or ommit argument to not use model logs
    if model_logs == "true" or model_logs == "True":
        model.activate_logs()
    
    all_debits = get_all_debits()

    # print(all_debits)

    compare_sums_of_debits( all_debits )

    create_debits_csv_file( all_debits )

    model.save_model()

if __name__ == '__main__':
    app()
