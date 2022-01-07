import csv


def get_csv_rows(file, del_headers=False):
        # reading csv file
    rows = []

    with open(file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        if del_headers:
            # extracting field names through first row
            fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    return rows

