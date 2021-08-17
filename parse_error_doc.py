import sys
import re

ERROR_FILE_PATH = 'full_error_doc.txt'

KEYWORDS = ["Message name", "Printing example",
            "Meaning", "Cause", "Remark", "Action", "Note", "Error code"]
IGNORE_KEYWORDS = ["IM 32P02B10-01EN"]


class PrintingExample:
    def __init__(self, printing_example, meaning, cause, remark, action, note, error):
        self.printing_example = printing_example
        self.meaning = meaning
        self.cause = cause
        self.remark = remark
        self.action = action
        self.note = note
        self.error_code = error


class ErrorStructure:
    def __init__(self, id, message_name, printing):
        self.id = id
        self.message_name = message_name
        self.printing_example = printing


#Test string is serialnumber format is No.XXXX
def is_serial_number(str):
    regex = r"^No.\d{4}$"
    if re.match(regex, str):
        return True
    else:
        return False


def is_matching_keyword(str, keyword):
    regex = r"^" + keyword
    if re.match(regex, str):
        return True
    else:
        return False


def is_keyword(str):
    for key in KEYWORDS:
        if is_matching_keyword(str, key) or is_serial_number(str):
            return True

    return False


def parse_error_file(filepath):
    with open(filepath, encoding="utf8") as fp:
        line = fp.readline()
        current_key = ""
        value = ""
        error_dic = {}
        while line:
            line = fp.readline()
            if(is_serial_number(line)):
                if(current_key != ""):
                    error_dic[current_key[3:]] = value

                current_key = line.strip()
                value = ""
            else:
                value += line

        error_dic[current_key[3:]] = value

    return error_dic


def get_response_as_string(keyword, value):
    str1 = " "
    str1 = str1.join(value)
    if(len(str1) > len(keyword)):
        str1 = str1[len(keyword):]
    return str1.strip()


def parse_value(values, keyword):
    response_key = ""
    response_value = []

    index = 0
    while index < len(values):
        line = values[index]
        if(is_matching_keyword(line, keyword)):
            if(response_key != ""):
                break

            response_key = line.strip()
            response_value.append(line.strip())
            index += 1
        elif(is_keyword(line)):
            break
        elif(is_matching_keyword(line, IGNORE_KEYWORDS[0])):
            index += 1
        else:
            response_value.append(line.strip())
            index += 1

    response = get_response_as_string(keyword, response_value)
    return index, response


def parse_printing_example(str):
    index = 0
    next_index, _printing = parse_value(str, "Printing example")
    index += next_index
    _meaning = ""
    _cause = ""
    _remark = ""
    _action = ""
    _note = ""
    _error_code = ""

    while(index < len(str)):
        if(is_matching_keyword(str[index], "Meaning")):
            next_index, _meaning = parse_value(str[index:], "Meaning")
            index += next_index
        elif(is_matching_keyword(str[index], "Cause")):
            next_index, _cause = parse_value(str[index:], "Cause")
            index += next_index
        elif(is_matching_keyword(str[index], "Remark")):
            next_index, _remark = parse_value(str[index:], "Remark")
            index += next_index
        elif(is_matching_keyword(str[index], "Action")):
            next_index, _action = parse_value(str[index:], "Action")
            index += next_index
        elif(is_matching_keyword(str[index], "Note")):
            next_index, _note = parse_value(str[index:], "Note")
            index += next_index
        elif(is_matching_keyword(str[index], "Error code")):
            next_index, _error_code = parse_value(str[index:], "Error code")
            index += next_index
        elif(is_matching_keyword(str[index], "Printing example")):
            break
        elif(is_matching_keyword(str[index], IGNORE_KEYWORDS[0])):
            index += 1
        else:
            index += 1

    return index, PrintingExample(_printing, _meaning, _cause, _remark, _action, _note, _error_code)


def parse_error_structure(error_dic):
    full_dict = {}
    for(key, value) in error_dic.items():
        values = value.split("\n")
        index = 0
        printing_example = []
        _message = ""
        while index < len(values):
            line = values[index]
            if(is_matching_keyword(line, "Message name")):
                next_index, _message = parse_value(
                    values[index:], "Message name")
                index += next_index
            elif(is_matching_keyword(line, "Printing example")):
                next_index, _printing = parse_printing_example(values[index:])
                index += next_index
                printing_example.append(_printing)
            elif(is_matching_keyword(line, IGNORE_KEYWORDS[0])):
                index += 1
            else:
                print("Unknown keyword: for " + key + " " + line)
                index += 1

        error = ErrorStructure(key, _message, printing_example)
        full_dict[key] = error
    return full_dict


def print_contents(dic):
    for (key, value) in dic.items():
        print("--------------------------------- " + key +
              " -----------------------------------------")
        print("Error Id: " + value.id + "\nMessage Name: " +
              value.message_name)
        for printing in value.printing_example:
            print("Printing Example: " + printing.printing_example)
            print("\tMeaning: " + printing.meaning)
            print("\tCause: " + printing.cause)
            print("\tRemark: " + printing.remark)
            print("\tAction: " + printing.action)
            print("\tNote: " + printing.note)
            print("\tError code: " + printing.error_code)


def main(in_file):
    error_dic = parse_error_structure(parse_error_file(in_file))
    print_contents(error_dic)


if __name__ == "__main__":
    if(len(sys.argv) == 2):
        in_file = sys.argv[1]
    else:
        in_file = ERROR_FILE_PATH

    main(in_file)
