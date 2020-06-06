#!/usr/bin/env python3

import argparse
import sys


def parse_line(line, header):
    """ Parse line into dictionary """
    spline = line.strip().split(';')
    data = {k: v for k, v in zip(header, spline)}
    return data


def to_tuple(data):
    """ Convert a data dictionary to key, values tuple """
    keys = ['Municipality_code', 'Municipality_name', 'Province']
    values = ['Total_reported', 'Hospital_admission', 'Deceased']

    key = tuple(data[x] for x in keys)
    val = tuple(data[x] for x in values)

    return key, val
           

def calculate_diff(previous, current):
    """ Caculcate the differences between the previous and current values """
    diff = dict()

    # The date should be the current date
    diff['Date_of_report'] = current['Date_of_report']

    # The values that are the same for previous and current
    identical = ['Municipality_code', 'Municipality_name', 'Province']
    for field in identical:
        assert previous[field] == current[field]
        diff[field] = current[field]

    # The values that can differ between previous and current
    different = ['Total_reported', 'Hospital_admission', 'Deceased']
    for field in different:
        p = int(previous[field])
        c = int(current[field])
        # The previous value should be less or equal to the current
        msg = 'WARN: {f} has decreased by {d} for {m} between {p} and {c}'
        if p > c:
            print(msg.format(f=field, m=current['Municipality_name'],
                                       p=previous['Date_of_report'],
                                       d=p-c,
                                       c=current['Date_of_report']),
                                       file=sys.stderr)
        diff[field] = c-p
    
    return diff

def main(args):
    # Store the previous values
    previous = dict()
    
    with open(args.input) as fin:
        header = next(fin).strip().split(';')
        assert header == ['Date_of_report', 'Municipality_code',
                          'Municipality_name', 'Province', 'Total_reported',
                          'Hospital_admission', 'Deceased']

        print(*header, sep=';')
        for line in fin:
            data = parse_line(line, header)
            keys, values = to_tuple(data)

            # If this is the first time we see these keys
            if keys not in previous:
                print(*(data[x] for x in header), sep=';')
                previous[keys] = data
            # IF we have seen these keys before, we print the difference
            else:
                diff = calculate_diff(previous[keys], data)
                print(*(diff[x] for x in header), sep=';')
                previous[keys] = data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=('Convert COVID-19_aantallen_gemeente_cumulatief.csv '
                     'to daily values')
    )

    parser.add_argument('--input')

    arguments = parser.parse_args()
    main(arguments)
