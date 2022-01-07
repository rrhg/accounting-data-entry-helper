import csv


def append_csv_row_to_file( alist, afile ):

    # with open(output_file, 'w') as f:
    """ before this, it was adding an empty line between csv lines # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows """
    with open( afile, 'a', newline='\n', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        # w = csv.writer(f)
        # w.writerows(csv_rows)
        w.writerow( alist )