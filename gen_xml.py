from xml.etree import ElementTree as ET
from io import BytesIO
from helpers import make_response_signature


def make_xml_response(attrs_dict, result_code, command='check'):
    response = ET.Element('response')
    txn_id = ET.SubElement(response, 'txn_id')
    txn_id.text = attrs_dict['txn_id']

    if command == 'pay' and result_code == '0':
        bill_reg_id = ET.SubElement(response, 'bill_reg_id')
        bill_reg_id.text = str(attrs_dict['transaction_id'])
        payment_sum = ET.SubElement(response, 'sum')
        payment_sum.text = attrs_dict['sum']

    result = ET.SubElement(response, 'result')
    result.text = result_code

    payment_signature = ET.SubElement(response, 'signature')
    payment_signature.text = make_response_signature(attrs_dict,
                                                     result_code,
                                                     command)

    et = ET.ElementTree(response)
    f = BytesIO()
    et.write(f, encoding='utf-8', xml_declaration=True)
    return f.getvalue()
