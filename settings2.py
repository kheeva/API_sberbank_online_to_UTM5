ip_white_list = [
    '127.0.0.1',
]

required_query_params = [
    'command',
    'account',
    'txn_id',
    'signature'
]

db_cfg = {
    'host': 'localhost',
    'port': 3306,
    'user': 'db_user',
    'password': 'db_password',
    'database': 'UTM5',
    'charset': 'utf8'
}

ourfa_args = ['-x', 'xml',
              '-H', 'localhost',
              '-l', 'bill_user',
              '-P', 'bill_pass',
              '-S', 'rsa_cert',
              '-a', 'add_payment',
              '-payment_method', '10',
              '-turn_on_inet', '1']

results = {
    'success': '0',
    'temp_err': '1',
    'wrong_login': '4',
    'id_not_found': '5',
    'forbidden': '7',
    'tech_forbidden': '8',
    'id_inactive': '79',
}

