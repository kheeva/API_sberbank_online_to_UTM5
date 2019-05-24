from controller import App

import commands
from helpers import parse_get_params, is_correct_query_params
from settings import ip_white_list, required_query_params


application = App(ip_white_list)


@application.register_handler('^/sberbank_online_api_type_a/$')
def sber_url_handler(environ, url_params):
    get_params = parse_get_params(environ['QUERY_STRING'])

    if not is_correct_query_params(get_params, required_query_params):
        return b'412: BAD PARAMS', 412, {}

    return getattr(commands, get_params['command'])(get_params)
