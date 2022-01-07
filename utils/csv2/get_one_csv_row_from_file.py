import csv


def get_one_csv_row_from_file(file):
    # rows = []
    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields_or_1st_line = next(csvreader) # just in case htere are headers
    
        return next(csvreader)

        # extracting each data row one by one
        # for row in csvreader:
            # rows.append(row)