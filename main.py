import sys
from parse_csv_file import parse_csv

CSV_IN_FILE = 'in_file.csv'
CSV_OUT_FILE = 'out_file.csv'

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    else:
        in_file = CSV_IN_FILE
        out_file = CSV_OUT_FILE

    parse_csv(in_file, out_file)