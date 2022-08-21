from config import client, debit, credit
from rich.console import Console
from utils.other import ask_to_continue

red = Console(style="red")


def extract_section_lines(lines, trans_type=debit):
    NUMBER_OF_LINES = 0
    REFERENCE_FOR_TRANSACTIONS = trans_type # Which are not checks
    AMOUNTS_FOR_CSV_FILE = []

    LINE_NUMBER = 0 # will not include blank lines, undecoded, or before STARTING LINE FOR DEBITS or after ENDING LINE FOR DEBITS 
    STARTING_LINE = 0
    FOUND_STARTING_LINE = False
    ENDING_LINE = 0
    FOUND_ENDING_LINE = False
    STOP_SEARCHING_FOR_ENDING_LINE = False


    is_1st_line = client.is_1st_line_of_debits
    if trans_type == credit:
        is_1st_line = client.is_1st_line_of_credits

    is_last_line = client.is_last_line_of_debits
    if trans_type == credit:
        is_last_line = client.is_last_line_of_credits


    def find_starting_and_ending_line(line, previous_line):
        # global LINE_NUMBER # no need bc we are not changing its value here
        nonlocal FOUND_STARTING_LINE
        nonlocal FOUND_ENDING_LINE
        nonlocal STARTING_LINE
        nonlocal ENDING_LINE
        nonlocal STOP_SEARCHING_FOR_ENDING_LINE

        if (    FOUND_STARTING_LINE == False
                and
                is_1st_line(line, previous_line)
            ):
            print()
            red.print(' ==> Found starting '+ trans_type +' line. : ')
            print( line)
            print()
            FOUND_STARTING_LINE = True
            STARTING_LINE = LINE_NUMBER

        elif (    FOUND_ENDING_LINE == False
                and
                is_last_line(line, previous_line)
            ):
            print()
            red.print(' ==> Found ending '+ trans_type +' line. : ')
            print( line)
            print()
            ENDING_LINE = LINE_NUMBER
            FOUND_ENDING_LINE = True

        if (
                FOUND_ENDING_LINE == True
                and
                (ENDING_LINE + 1) == LINE_NUMBER
        ):
            # so that last line is included
            STOP_SEARCHING_FOR_ENDING_LINE = True

    cleaned_lines = []
    previous_line = ''

    for line in lines: 
        LINE_NUMBER +=1
        find_starting_and_ending_line(line, previous_line)

        # this might be indented when finish functions
        if (    FOUND_STARTING_LINE == True
                and
                STOP_SEARCHING_FOR_ENDING_LINE == False
                # and decoded and is_not_a_blanc_line(line)
            ):
            # print(line)
            cleaned_lines.append(line)
        previous_line = line

    if not FOUND_STARTING_LINE:
        red.print('\n Did not found starting '+ trans_type +' line. ')
        red.print('Posible solution: In client functions change "is_1st_line_of_'+ trans_type + 's()"')
        ask_to_continue()
    elif not FOUND_ENDING_LINE:
        red.print('\n Did not found ending '+ trans_type +' line. : ')
        red.print('Posible solution: In client functions change "is_last_line_of_'+ trans_type + 's()"')
        ask_to_continue

    return cleaned_lines



