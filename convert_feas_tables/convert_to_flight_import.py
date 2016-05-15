"""
Author: Markus W. Hofmann
Initial Date: May 9, 2016

License: MIT

Description:

"""

import os
import csv

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
                is_matching_filter=True
    else:
        is_matching_filter = True
    return is_matching_filter


def open_csv(file_path, row_filter=None):
    dict_list = list()
    with open(file_path, 'rb') as file_handle:
        dict_reader = csv.DictReader(file_handle)
        for row in dict_reader:
            if matches_filter(row, row_filter):
                dict_list.append(row)
    return dict_list


def convert_time(input_date: str, input_time: str):
    """
    Input is 04/01/2007 (MM/DD/YYYY) and 12/30/1899 13:35:00 (WRONG DATE HH:MM)

    Output shall be 10.02.2016 13:00 (DD.MM.YYYY HH:MM)
    """
    output = ''

    date_part = input_date.split('/')
    output = date_part[1] + '.' + date_part[0] + '.' + date_part[2]
    time_string = input_time[input_time.find(' '):]
    output += time_string[:-3]
    return output


def convert_feas_export(directory_path):
    flight_main = open_csv(os.path.join(directory_path, "Flight.csv"), row_filter=('SDate', ['2014', '2015', '2016']))

    tow_dict = None
    for row in flight_main:
        if row['MasterRecord'] == '0':
            tow_dict = row  # tow row comes first
            continue
        else:
            tow_dict = dict()
            flight_dict = row

        get_flight_import_dict(flight_dict.get('LK', '') + '-' + flight_dict.get('KZ'),
                               flight_dict.get('Pilot', ''),
                               flight_dict.get('Begleiter', ''),
                               convert_time(flight_dict.get('SDate', ''), flight_dict.get('STime')),
                               flight_dict.get('StartOrt', ''),
                               convert_time(flight_dict.get('LDate', ''), flight_dict.get('LTime')),
                               flight_dict.get('LandeOrt', ''),
                               flight_dict.get('Dauer', ''),
                               '1',
                               convert_starttype(flight_dict.get('SA', '')),
                               flight_dict.get('', ''),  # TODO
                               flight_dict.get('', ''),  # TODO
                               flight_dict.get('', ''),  # TODO tow height
                               get_tow_time(tow_dict.get('STime', ''), tow_dict.get('LTime')),
                               flight_dict.get('imported', ''),
                               tow_dict.get('LK', '') + '-' + tow_dict.get('KZ'),
                               tow_dict.get('Pilot', ''),
                               convert_type(tow_dict.get('FA', '')),
                               '',
                               tow_dict.get('Muster', ''),
                               '',
                               '',
                               '',
                               '',
                               '',
                               '',
                               convert_charge(tow_dict.get('', '')),
                               "255"
                               )


def write_flight_import_dict(dict_list):
    output_file_path = os.path.join(os.path.dirname(__file__), 'flight_import.csv')
    with open(output_file_path, 'wb') as flight_import_csv:
        dict_writer = csv.DictWriter(flight_import_csv, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)
