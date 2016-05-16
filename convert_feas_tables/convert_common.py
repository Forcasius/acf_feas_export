"""
Author: Markus W. Hofmann
Initial Date: 5/16/16

License: MIT

Description:

"""
import os
import csv


def matches_filter(input_dict, row_filter):
    is_matching_filter = False
    if row_filter:
        matching_field = input_dict.get(row_filter[0], '')
        for criteria in row_filter[1]:
            if criteria in matching_field:
                is_matching_filter = True
    else:
        is_matching_filter = True
    return is_matching_filter


def open_csv(file_path, row_filter=None):
    dict_list = list()
    with open(file_path, 'r') as file_handle:
        dict_reader = csv.DictReader(file_handle, delimiter=';')
        for row in dict_reader:
            if matches_filter(row, row_filter):
                dict_list.append(row)
    return dict_list


def open_xlsx(file_path, row_filter=None):
    dict_list = list()
    import pyexcel

    r = pyexcel.SeriesReader(file_path)
    # make a filter function
    # filter_func = lambda row_index: row_index < 124 or row_index > 141
    # apply the filter on the reader
    # r.filter(pyexcel.filters.RowIndexFilter(filter_func))
    # get the data
    dict_list = pyexcel.utils.to_records(r)
    return dict_list


def write_flight_import_dict(dict_list: list, fieldnames: list, file_name: str):
    output_file_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.isfile(output_file_path):
        os.rename(output_file_path, output_file_path + '.bak')
    with open(output_file_path, 'w', encoding='ISO-8859-1') as flight_import_csv:
        dict_writer = csv.DictWriter(flight_import_csv, fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)

