import os
import sys
import argparse
import re
import pandas as pd


pat = re.compile(r''
                 '(?P<ip>\d+.\d+.\d+.\d+)\s-\s-\s' #IP address
                 '\[(?P<datetime>.+)\]\s' #datetime
                 '"GET\s(?P<file>.+)\s\w+/.+"\s\d+\s' #requested file
                 '[\d\-]+\s"(?P<referrer>.+)"\s' #referrer
                 '"(?P<user_agent>.+)"' #user agent
                 )


def line_parser(list_input):
    processed_output = []
    for line in list_input:
        match = pat.search(line)
        if match:
            d = match.groupdict()
            processed_output.append(d)
    return processed_output


def load_dict(list_of_dicts):
    # load list of dictionaries into pandas DataFrame
    df = pd.DataFrame.from_records(list_of_dicts)
    return df


def main(args):
    cmd_parser = argparse.ArgumentParser(description='Parse arguments to log parser', prog='logparse')
    cmd_parser.add_argument('file_input', type=str)
    opts = cmd_parser.parse_args(args)
    f = open(opts.file_input)
    log_lines = f.readlines()
    f.close()
    output = line_parser(log_lines)
    print(output)
    data = load_dict(output)
    print(data)


if __name__ == '__main__':    
    main(sys.argv[1:])