#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Markus W. Hofmann
Initial Date: May 9, 2016

License: MIT

Description:

"""
import logging
import os
from convert_feas_tables.convert_common import open_csv, write_flight_import_dict


fieldnames = [
    'title', 'lastname', 'firstname', 'street', 'zipcode', 'town', 'cyid', 'email', 'gender', 'birthday', 'homenumber',
    'mobilenumber', 'phonenumber', 'phonenumber2', 'memberid', 'msid', 'memberbegin', 'memberend', 'key1designation',
    'key2designation', 'comment', 'bankcode', 'bankaccount', 'bankaccountname', 'bankaccountinfo', 'lettertitle',
    'directdebitauth', 'iban', 'bic', 'mandate', 'mandatedate', 'function_1', 'function_2', 'function_3', 'function_4',
    'function_5', 'function_6', 'function_7', 'function_8', 'function_9', 'function_10', 'sector_1', 'sector_2',
    'sector_3', 'sector_4', 'sector_5', 'sector_6', 'sector_7', 'sector_8', 'sector_9', 'sector_10', 'nickname',
    'gpl_license', 'gpl_licenseno', 'gpl_from', 'gpl_starttype_w', 'gpl_starttype_f', 'gpl_starttype_e', 'gpl_acro',
    'gpl_pax', 'gpl_tmg_tow', 'spl_com_ops', 'tmg', 'sep', 'sep_validto', 'nq', 'ir_sep', 'ir_sep_validto', 'ir_mep',
    'ir_mep_validto', 'mep', 'mep_validto', 'ul_license', 'ul_licenseno', 'ul_valid', 'ul_validto', 'ul_from',
    'ppla_license', 'ppla_licenseno', 'ppla_from', 'gpl_flightinstructor', 'gpl_flightinstructor_validto',
    'gpl_fi_seminar', 'ul_flightinstructor', 'ul_flightinstructor_validto', 'ul_fi_seminar', 'ppl_flightinstructor',
    'ppl_flightinstructor_validto', 'ppl_fi_seminar', 'ppl_cri_sep', 'ppl_cri_sep_validto', 'ppl_cri_tmg',
    'ppl_cri_tmg_validto', 'medicalclass1', 'medicalclass1no', 'medicalclass2', 'medicalclass2no', 'medicallapl',
    'medicallaplno', 'ppla_tmg', 'ppla_tmg_validto', 'ppl_tow_sep', 'ppl_tow_tmg', 'ppl_pax', 'ul_tow', 'ul_pax',
    'reliabilitycheck_validto', 'ppl_acro', 'radio_telephony', 'radio_telephony_no', 'english_level',
    'english_level_validto'
]


def get_flight_import_dict(title, lastname, firstname, street, zipcode, town, cyid, email, gender, birthday, homenumber,
                           mobilenumber, phonenumber, phonenumber2, memberid, msid, memberbegin, memberend,
                           key1designation, key2designation, comment, bankcode, bankaccount, bankaccountname,
                           bankaccountinfo, lettertitle, directdebitauth, iban, bic, mandate, mandatedate, function_1,
                           function_2, function_3, function_4, function_5, function_6, function_7, function_8,
                           function_9, function_10, sector_1, sector_2, sector_3, sector_4, sector_5, sector_6,
                           sector_7, sector_8, sector_9, sector_10, nickname, gpl_license, gpl_licenseno, gpl_from,
                           gpl_starttype_w, gpl_starttype_f, gpl_starttype_e, gpl_acro, gpl_pax, gpl_tmg_tow,
                           spl_com_ops, tmg, sep, sep_validto, nq, ir_sep, ir_sep_validto, ir_mep, ir_mep_validto, mep,
                           mep_validto, ul_license, ul_licenseno, ul_valid, ul_validto, ul_from, ppla_license,
                           ppla_licenseno, ppla_from, gpl_flightinstructor, gpl_flightinstructor_validto,
                           gpl_fi_seminar, ul_flightinstructor, ul_flightinstructor_validto, ul_fi_seminar,
                           ppl_flightinstructor, ppl_flightinstructor_validto, ppl_fi_seminar, ppl_cri_sep,
                           ppl_cri_sep_validto, ppl_cri_tmg, ppl_cri_tmg_validto, medicalclass1, medicalclass1no,
                           medicalclass2, medicalclass2no, medicallapl, medicallaplno, ppla_tmg, ppla_tmg_validto,
                           ppl_tow_sep, ppl_tow_tmg, ppl_pax, ul_tow, ul_pax, reliabilitycheck_validto, ppl_acro,
                           radio_telephony, radio_telephony_no, english_level, english_level_validto):
    result = dict(
        title=title,
        lastname=lastname,
        firstname=firstname,
        street=street,
        zipcode=zipcode,
        town=town,
        cyid=cyid,
        email=email,
        gender=gender,
        birthday=birthday,
        homenumber=homenumber,
        mobilenumber=mobilenumber,
        phonenumber=phonenumber,
        phonenumber2=phonenumber2,
        memberid=memberid,
        msid=msid,
        memberbegin=memberbegin,
        memberend=memberend,
        key1designation=key1designation,
        key2designation=key2designation,
        comment=comment,
        bankcode=bankcode,
        bankaccount=bankaccount,
        bankaccountname=bankaccountname,
        bankaccountinfo=bankaccountinfo,
        lettertitle=lettertitle,
        directdebitauth=directdebitauth,
        iban=iban,
        bic=bic,
        mandate=mandate,
        mandatedate=mandatedate,
        function_1=function_1,
        function_2=function_2,
        function_3=function_3,
        function_4=function_4,
        function_5=function_5,
        function_6=function_6,
        function_7=function_7,
        function_8=function_8,
        function_9=function_9,
        function_10=function_10,
        sector_1=sector_1,
        sector_2=sector_2,
        sector_3=sector_3,
        sector_4=sector_4,
        sector_5=sector_5,
        sector_6=sector_6,
        sector_7=sector_7,
        sector_8=sector_8,
        sector_9=sector_9,
        sector_10=sector_10,
        nickname=nickname,
        gpl_license=gpl_license,
        gpl_licenseno=gpl_licenseno,
        gpl_from=gpl_from,
        gpl_starttype_w=gpl_starttype_w,
        gpl_starttype_f=gpl_starttype_f,
        gpl_starttype_e=gpl_starttype_e,
        gpl_acro=gpl_acro,
        gpl_pax=gpl_pax,
        gpl_tmg_tow=gpl_tmg_tow,
        spl_com_ops=spl_com_ops,
        tmg=tmg,
        sep=sep,
        sep_validto=sep_validto,
        nq=nq,
        ir_sep=ir_sep,
        ir_sep_validto=ir_sep_validto,
        ir_mep=ir_mep,
        ir_mep_validto=ir_mep_validto,
        mep=mep,
        mep_validto=mep_validto,
        ul_license=ul_license,
        ul_licenseno=ul_licenseno,
        ul_valid=ul_valid,
        ul_validto=ul_validto,
        ul_from=ul_from,
        ppla_license=ppla_license,
        ppla_licenseno=ppla_licenseno,
        ppla_from=ppla_from,
        gpl_flightinstructor=gpl_flightinstructor,
        gpl_flightinstructor_validto=gpl_flightinstructor_validto,
        gpl_fi_seminar=gpl_fi_seminar,
        ul_flightinstructor=ul_flightinstructor,
        ul_flightinstructor_validto=ul_flightinstructor_validto,
        ul_fi_seminar=ul_fi_seminar,
        ppl_flightinstructor=ppl_flightinstructor,
        ppl_flightinstructor_validto=ppl_flightinstructor_validto,
        ppl_fi_seminar=ppl_fi_seminar,
        ppl_cri_sep=ppl_cri_sep,
        ppl_cri_sep_validto=ppl_cri_sep_validto,
        ppl_cri_tmg=ppl_cri_tmg,
        ppl_cri_tmg_validto=ppl_cri_tmg_validto,
        medicalclass1=medicalclass1,
        medicalclass1no=medicalclass1no,
        medicalclass2=medicalclass2,
        medicalclass2no=medicalclass2no,
        medicallapl=medicallapl,
        medicallaplno=medicallaplno,
        ppla_tmg=ppla_tmg,
        ppla_tmg_validto=ppla_tmg_validto,
        ppl_tow_sep=ppl_tow_sep,
        ppl_tow_tmg=ppl_tow_tmg,
        ppl_pax=ppl_pax,
        ul_tow=ul_tow,
        ul_pax=ul_pax,
        reliabilitycheck_validto=reliabilitycheck_validto,
        ppl_acro=ppl_acro,
        radio_telephony=radio_telephony,
        radio_telephony_no=radio_telephony_no,
        english_level=english_level,
        english_level_validto=english_level_validto
    )
    return result


def get_member_status(status: str):
    if status == 'fördernd':
        result_state = '5'
    elif status == 'aktiv':
        result_state = '1'
    elif status == 'teilaktiv':
        result_state = '2'
    else:
        result_state = '6'
    return result_state


def has_licence(licence: str, licence_string: str):
    return str(int(licence in licence_string))


def convert_member_import(directory_path: str):
    members_main = open_csv(os.path.join(directory_path, "TBL_Members_Main.csv"))
    full_member_list = list()

    try:
        for member in members_main:
            member_import_dict = get_flight_import_dict('',
                                                        member.get('Name'),
                                                        member.get('Vorname'),
                                                        '',
                                                        '',
                                                        '',
                                                        '1',  # country code
                                                        member.get('EmailAdress'),
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        member.get('ID'),
                                                        get_member_status(member.get('Status')),
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        member.get('Comment'),
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        has_licence('C', member.get('LizenzInhaber')),  # GPL
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        has_licence('A', member.get('SchleppLizenzen')),  # GPL tow
                                                        '',
                                                        has_licence('B', member.get('LizenzInhaber')),  # tmg
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        has_licence('F', member.get('LizenzInhaber')),  # ul
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        has_licence('A', member.get('LizenzInhaber')),  # ppl-a
                                                        '',
                                                        '',
                                                        has_licence('C', member.get('LehrerLizenzen')),  # gpl inst
                                                        '',
                                                        '',
                                                        has_licence('F', member.get('LehrerLizenzen')),  # ul inst
                                                        '',
                                                        '',
                                                        has_licence('A', member.get('LehrerLizenzen')),  # ppl inst
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        has_licence('B', member.get('SchleppLizenzen')),  # tmg tow
                                                        '',
                                                        has_licence('F', member.get('SchleppLizenzen')),  # ul tow
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        '',
                                                        ''
                                                        )
            full_member_list.append(member_import_dict)
        write_flight_import_dict(full_member_list, fieldnames, 'member_import.csv')
    except Exception:
        logging.exception("Exception during convertion")
    finally:
        logging.info("Number of converted members: %d", len(full_member_list))


if __name__ == '__main__':
    log_path = os.path.join(os.path.dirname(__file__), 'log.txt')
    logging.basicConfig(level=logging.DEBUG, filename=log_path, filemode='w')
    logging.getLogger().addHandler(logging.StreamHandler())
    convert_member_import(os.path.dirname(__file__))
