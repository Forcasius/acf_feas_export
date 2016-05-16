"""
Author: Markus W. Hofmann
Initial Date: May 9, 2016

License: MIT

Description:

"""

import os
import csv
import logging

fieldnames = ["callsign", "pilotname", "attendantname", "departuretime", "departurelocation", "arrivaltime",
              "arrivallocation", "flighttime", "landingcount", "starttype", "motorstart", "motorend", "towheight",
              "towtime", "comment", "towcallsign", "towpilotname", "ftid", "planewkz", "planedesignation",
              "attendantname2", "attendantname3", "offblock", "onblock", "km", "wid", "chargemode", "invoiced"]


def get_flight_import_dict(callsign, pilotname, attendantname, departuretime, departurelocation, arrivaltime,
                           arrivallocation, flighttime, landingcount, starttype, motorstart, motorend, towheight,
                           towtime, comment, towcallsign, towpilotname, ftid, planewkz, planedesignation,
                           attendantname2, attendantname3, offblock, onblock, km, wid, chargemode, invoiced):
    result = dict(
        callsign=callsign,
        pilotname=pilotname,
        attendantname=attendantname,
        departuretime=departuretime,
        departurelocation=departurelocation,
        arrivaltime=arrivaltime,
        arrivallocation=arrivallocation,
        flighttime=flighttime,
        landingcount=landingcount,
        starttype=starttype,
        motorstart=motorstart,
        motorend=motorend,
        towheight=towheight,
        towtime=towtime,
        comment=comment,
        towcallsign=towcallsign,
        towpilotname=towpilotname,
        ftid=ftid,
        planewkz=planewkz,
        planedesignation=planedesignation,
        attendantname2=attendantname2,
        attendantname3=attendantname3,
        offblock=offblock,
        onblock=onblock,
        km=km,
        wid=wid,
        chargemode=chargemode,
        invoiced=invoiced
    )
    return result


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


def convert_time(input_date: str, input_time: str):
    """
    Input is 04/01/2007 (MM/DD/YYYY) and 12/30/1899 13:35:00 (WRONG DATE HH:MM)

    Output shall be 10.02.2016 13:00 (DD.MM.YYYY HH:MM)
    """
    date_part = input_date.split('/')
    if not len(date_part) == 3:
        logging.error("Date Format is wrong: %s %s", input_date, input_time)
    output = date_part[1] + '.' + date_part[0] + '.' + date_part[2]
    time_string = input_time[input_time.find(' '):]
    output += time_string[:-3]
    return output


def convert_starttype(feas_start_type):
    result = None
    if feas_start_type == 'E':
        result = '1'
    elif feas_start_type == 'F':
        result = '3'
    return result


def convert_type(feas_type):
    result = None

    if feas_type == 'F':
        result = '15'  # Fremdflug
    elif feas_type == 'G':
        result = '4'  # Passagierflug == Gastflug
    elif feas_type == 'L':
        result = '14'  # Luftrettung
    elif feas_type == 'N':
        result = '10'  # Normalflug == Privatflug
    elif feas_type == 'R':
        result = '3'
    elif feas_type == 'S':
        result = '8'
    elif feas_type == 'V':
        result = '13'  # Vereinsflug
    elif feas_type == 'W':
        result = '2'
    return result


def convert_charge(feas_type: str, flight: dict):
    result = None
    if feas_type == 'F':
        result = '1'  # Fremdflug
    elif feas_type == 'G':
        result = '4'  # Passagierflug == Gastflug
    elif feas_type == 'L':
        result = '1'  # Luftrettung
    elif feas_type == 'N':
        result = '2'  # Normalflug == Privatflug
    elif feas_type == 'R':
        result = '2'
    elif feas_type == 'S':
        if flight.get('Begleiter', '') == '':
            result = '2'
        else:
            result = '3'
    elif feas_type == 'V':
        result = '1'  # Vereinsflug
    elif feas_type == 'W':
        result = '1'
    return result


def get_dict_for_flight_id(search_id: str, input_dict: list, column_name='ID'):
    found_flight = None
    for flight in input_dict:
        if search_id == flight.get(column_name, ''):
            found_flight = flight
    return found_flight


def convert_feas_export(directory_path: str):
    flight_main = open_csv(os.path.join(directory_path, "TBL_Flight_Main.csv"),
                           row_filter=('SDate', ['2014', '2015', '2016']))
    flight_payment = open_csv(os.path.join(directory_path, "TBL_Flight_Payment.csv"))
    members = open_csv(os.path.join(directory_path, "TBL_Members_Main.csv"))

    full_flight_list = list()

    try:
        for flight in flight_main:
            slave_record_id = flight['SlaveRecordID']
            if flight['MasterRecord'] == '1' and not slave_record_id == '0':  # The slave is always the tow flight
                tow_flight_dict = get_dict_for_flight_id(slave_record_id, flight_main)
                flight_dict = flight
                tow_pay_dict = get_dict_for_flight_id(flight['ID'], flight_payment, 'Index')
                sanity_check(flight_dict, tow_flight_dict)
            elif flight['MasterRecord'] == '0':
                continue  # Skip the tow plane!
            else:  # it flies on its own!
                tow_flight_dict = dict()
                tow_pay_dict = dict()
                flight_dict = flight

            flight_import_dict = get_flight_import_dict(assemble_call_sign(flight_dict.get('LK'), flight_dict.get('KZ')),
                                                        get_full_name(flight_dict.get('Pilot', ''), members),
                                                        get_full_name(flight_dict.get('Begleiter', ''), members),
                                                        convert_time(flight_dict.get('SDate', ''),
                                                                     flight_dict.get('STime')),
                                                        flight_dict.get('StartOrt', ''),
                                                        convert_time(flight_dict.get('LDate', ''),
                                                                     flight_dict.get('LTime')),
                                                        flight_dict.get('LandeOrt', ''),
                                                        flight_dict.get('Dauer', ''),
                                                        '1',
                                                        convert_starttype(flight_dict.get('SA', '')),
                                                        flight_dict.get('', ''),  # TODO ?
                                                        flight_dict.get('', ''),  # TODO ?
                                                        tow_pay_dict.get('TowPeak', ''),  # TODO tow height
                                                        tow_flight_dict.get('Dauer', ''),
                                                        'imported from FEAS',
                                                        assemble_call_sign(tow_flight_dict.get('LK'), tow_flight_dict.get('KZ')),
                                                        get_full_name(tow_flight_dict.get('Pilot', ''), members),
                                                        convert_type(flight_dict.get('FA', '')),
                                                        '',
                                                        flight_dict.get('Muster', ''),
                                                        get_full_name(tow_flight_dict.get('Begleiter', ''), members),
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        convert_charge(flight_dict.get('FA'), flight_dict),
                                                        "255"
                                                        )
            full_flight_list.append(flight_import_dict)
        write_flight_import_dict(full_flight_list)
    except Exception:
        logging.exception("Exception during convertion")
    finally:
        print("Number of converted flights: ", len(full_flight_list))


def get_full_name(short_name: str, members: list):
    name = short_name
    try:
        if short_name:
            name_parts = short_name.split(' ')
            last_name = name_parts[0]
            if len(name_parts) > 1:
                first_name_letter = name_parts[1].strip(' .')
            else:
                first_name_letter = ''

            for member in members:
                if last_name == member.get('Name'):
                    if first_name_letter == member.get('Vorname')[0]:
                        name = member.get('Name') + ', ' + member.get('Vorname')
                        break
    except Exception:
        logging.exception("Could not convert name %s", short_name)
    return name


def assemble_call_sign(lk, kz):
    if lk and kz:
        call_sign = lk + '-' + kz
    else:
        call_sign = ''
    return call_sign


def sanity_check(flight_dict, tow_flight_dict):
    if not flight_dict['STime'] == tow_flight_dict['STime']:
        logging.error('Tow flight and flight do not match! \n' + str(flight_dict) + '\n' + str(tow_flight_dict))


def write_flight_import_dict(dict_list: list):
    output_file_path = os.path.join(os.path.dirname(__file__), 'flight_import.csv')
    if os.path.isfile(output_file_path):
        os.rename(output_file_path, output_file_path + '.bak')
    with open(output_file_path, 'w', encoding='ISO-8859-1') as flight_import_csv:
        dict_writer = csv.DictWriter(flight_import_csv, fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


if __name__ == '__main__':
    convert_feas_export(os.path.dirname(__file__))
    log_path = os.path.join(os.path.dirname(__file__), 'log.txt')
    logging.basicConfig(level=logging.DEBUG, filename=log_path)
