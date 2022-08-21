from config import client, ACCOUNTS_JSON_FILE
from utils.json.write_list_to_json_file import write_list_to_json_file
from utils.csv2.get_csv_rows import get_csv_rows


def main():
    csv_file = client.file_with_new_accounts_to_import()
    rows = get_csv_rows( csv_file )
    """ csv rows have been converted to lists """

    accounts = []
    for r in rows:
        account_dict = client.convert_imported_account_csv_row_to_dict( r )
        accounts.append( account_dict )

    write_list_to_json_file( accounts, ACCOUNTS_JSON_FILE)
    

if __name__ == '__main__':
    main()
