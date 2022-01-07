from transactions.get_all import get_all_credits
from transactions.compare_sums_of_transactions import compare_sums_of_credits
from utils.csv2.create_output_csv_file import create_credits_csv_file


def main():

    all_credits = get_all_credits()

    # print(all_credits)

    compare_sums_of_credits( all_credits )

    create_credits_csv_file( all_credits )

if __name__ == '__main__':
    main()
