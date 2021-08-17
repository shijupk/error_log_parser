import sys
import csv

from parse_error_doc import parse_error_file, parse_error_structure

CSV_IN_FILE = 'in_file.csv'
ERROR_FILE_PATH = 'full_error_doc.txt'
CSV_OUT_FILE = 'out_file.csv'

fields = ['Timestamp', 'Quality', 'Type', 'ID',
          'Alarm State', 'Resource', 'Reference', 'Message', 'Message Name',
          'Printing example 1', 'Meaning 1', 'Cause 1', 'Remark 1', 'Action 1', 'Note 1',
          'Printing example 2', 'Meaning 2', 'Cause 2', 'Remark 2', 'Action 2', 'Note 2',
          'Printing example 3', 'Meaning 3', 'Cause 3', 'Remark 3', 'Action 3', 'Note 3']


def update_csv(in_file_name, out_file_name, error_dic):
    with open(in_file_name, 'r') as in_file:
        with open(out_file_name, 'w') as out_file:
            reader = csv.DictReader(in_file, fieldnames=fields)
            writer = csv.DictWriter(out_file, fieldnames=fields)

            for row in reader:
                #if first row continue
                if row['Timestamp'] == 'Timestamp':
                    writer.writeheader()
                    continue

                id = row['ID']
                id = id.split('-')[0]

                out_row = {'Timestamp': row['Timestamp'], 'Quality': row['Quality'], 'Type': row['Type'], 'ID': row['ID'], 'Alarm State': row['Alarm State'],
                           'Resource': row['Resource'], 'Reference': row['Reference'], 'Message': row['Message'], 'Message Name': '',
                           'Printing example 1': '', 'Meaning 1': '', 'Cause 1': '', 'Remark 1': '', 'Action 1': '', 'Note 1': '',
                           'Printing example 2': '', 'Meaning 2': '', 'Cause 2': '', 'Remark 2': '', 'Action 2': '', 'Note 2': '',
                           'Printing example 3': '', 'Meaning 3': '', 'Cause 3': '', 'Remark 3': '', 'Action 3': '', 'Note 3': ''}

                if id in error_dic:
                    out_row['Message Name'] = error_dic[id].message_name
                    printing_examples = error_dic[id].printing_example

                    i = 0
                    while(i < 3):
                        if i < len(printing_examples):
                            out_row['Printing example ' +
                                    str(i+1)] = printing_examples[i].printing_example
                            out_row['Meaning ' +
                                    str(i+1)] = printing_examples[i].meaning
                            out_row['Cause ' +
                                    str(i+1)] = printing_examples[i].cause
                            out_row['Remark ' +
                                    str(i+1)] = printing_examples[i].remark
                            out_row['Action ' +
                                    str(i+1)] = printing_examples[i].action
                            out_row['Note ' +
                                    str(i+1)] = printing_examples[i].note
                        else:
                            out_row['Printing example ' + str(i+1)] = ''
                            out_row['Meaning ' + str(i+1)] = ''
                            out_row['Cause ' + str(i+1)] = ''
                            out_row['Remark ' + str(i+1)] = ''
                            out_row['Action ' + str(i+1)] = ''
                            out_row['Note ' + str(i+1)] = ''
                        i += 1
                else:
                    out_row['Message Name'] = ''
                    out_row['Printing example 1'] = ''
                    out_row['Meaning 1'] = ''
                    out_row['Cause 1'] = ''
                    out_row['Remark 1'] = ''
                    out_row['Action 1'] = ''
                    out_row['Note 1'] = ''
                    out_row['Printing example 2'] = ''
                    out_row['Meaning 2'] = ''
                    out_row['Cause 2'] = ''
                    out_row['Remark 2'] = ''
                    out_row['Action 2'] = ''
                    out_row['Note 2'] = ''
                    out_row['Printing example 3'] = ''
                    out_row['Meaning 3'] = ''
                    out_row['Cause 3'] = ''
                    out_row['Remark 3'] = ''
                    out_row['Action 3'] = ''
                    out_row['Note 3'] = ''

                writer.writerow(out_row)


def parse_csv(in_file, out_file):
    error_dic = parse_error_structure(parse_error_file(ERROR_FILE_PATH))
    update_csv(in_file, out_file, error_dic)


if __name__ == "__main__":
    if(len(sys.argv) == 3):
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    else:
        in_file = CSV_IN_FILE
        out_file = CSV_OUT_FILE

    parse_csv(in_file, out_file)
