import subprocess
import xml.etree.ElementTree as ET
import datetime

from db import get_account_id
from settings import results, ourfa_args
from gen_xml import make_xml_response
from helpers import our_signature


def check(_q_attrs_dict):
    if not our_signature(_q_attrs_dict):
        return make_xml_response(_q_attrs_dict, results['forbidden'],), 403, {}

    if get_account_id(_q_attrs_dict['account']):
        return make_xml_response(_q_attrs_dict, results['success']), 200, {}

    return make_xml_response(_q_attrs_dict, results['id_not_found'],), 200, {}


def pay(_q_attrs_dict):
    if not our_signature(_q_attrs_dict):
        return make_xml_response(_q_attrs_dict, results['forbidden'],), 403, {}

    account_id = get_account_id(_q_attrs_dict['account'])

    if account_id:
        program_name = './ourfa_client'

        payment_args = [
            '-account_id', account_id,
            '-payment', _q_attrs_dict['sum'],
            '-payment_ext_number' ,_q_attrs_dict['txn_id'],
        ]

        if _q_attrs_dict.get('txn_date'):
            try:
                payment_date = datetime.datetime.strptime(
                    _q_attrs_dict['txn_date'],
                    '%Y%m%d%H%M%S'
                )
                payment_date = int(datetime.datetime.timestamp(payment_date))
                payment_date = str(payment_date)
            except Exception:
                print('wrong txn_date in GET params')
            else:
                payment_args.extend([
                    'payment_date',
                    payment_date
                ])

        command = [program_name]
        command.extend(ourfa_args)
        command.extend(payment_args)

        output = subprocess.Popen(
            command,
            stdout=subprocess.PIPE).communicate()[0]

        root = ET.fromstring(output)
        for i in root.iter('integer'):
            _q_attrs_dict['transaction_id'] = i.attrib['value']

        if _q_attrs_dict.get('transaction_id'):
            return make_xml_response(_q_attrs_dict,
                                     results['success'],
                                     'pay'), 200, {}

    return make_xml_response(_q_attrs_dict, results['temp_err'], 'pay'), 200, {}
