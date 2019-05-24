import hashlib
from settings import secret_word


def parse_get_params(params_str):
    _get_params = {}
    if not params_str:
        return _get_params

    for get_param in params_str.split('&'):
        get_param = get_param.split('=')
        param_name, param_value = get_param[0], get_param[1]
        _get_params[param_name] = param_value
    return _get_params


def is_correct_query_params(_params_dict, req_params):
    q_params = [_params_dict.get(param) is not None for param in req_params]
    return sum(q_params) == len(req_params) and _params_dict['command'] in ['check', 'pay']


def our_signature(_params):
    concat_params = ''.join([
        _params['command'],
        _params['txn_id'],
        _params['account'],
        _params['sum'],
        secret_word
    ])
    return hashlib.sha512(concat_params.encode()).hexdigest() == _params['signature']


def make_response_signature(_params, result_code, method='check'):
    concat_list = [
        _params['signature'],
        _params['txn_id'],
        result_code,
        secret_word
    ]
    if method == 'pay' and _params.get('bill_reg_id'):
        concat_list.insert(2, _params['bill_reg_id'])

    concat_params = ''.join(concat_list)
    return hashlib.sha512(concat_params.encode()).hexdigest()
