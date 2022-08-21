from rich.console import Console
from config import ACCOUNTS_JSON_FILE
from utils.json.get_list_from_json_file import get_list_from_json_file 
from utils.prompt_user_autocomplete import prompt_user_autocomplete

red = Console(style="red")
yellow = Console(style="yellow")


def get_chart_of_accounts():
    return get_list_from_json_file( ACCOUNTS_JSON_FILE )


def prompt_user_for_account_number():
    chart_of_accounts = get_chart_of_accounts()
    accounts_to_choose = [f"{a['number']} {a['name']}" for a in chart_of_accounts]
    red.print("\nChoose an account: " )
    chosen = prompt_user_autocomplete( ' : ', accounts_to_choose )
    account_number = chosen.split(' ')[0]
    return account_number

def get_account_name(number):
    chart = get_chart_of_accounts()
    return next(a['name'] for a in chart if a['number'] == number)