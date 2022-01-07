import csv


def write_rows_to_csv_file(output_file, csv_rows):
    # with open(output_file, 'w') as f:
    # remove empty lines # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
    with open(output_file, '+w', newline='\n', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        # w = csv.writer(f)
        w.writerows(csv_rows)

