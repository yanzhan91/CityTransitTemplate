import logging as log
import re

from flask import jsonify

from Constants import city_constants
from intents import CheckIntent
from intents import GetIntent
from intents import SetIntent


def webhook(request, city):
    agency, city_full, intent, param, user = get_default_params(city, request)

    log.info("city=%s" % city)
    log.info('param=%s' % param)
    log.info('intent=%s' % intent)
    log.info('user=%s' % user)

    if intent == 'CheckIntent':
        message = __check(agency, city_full, param)
    elif intent == 'SetIntent':
        message = __set(agency, city_full, param, user)
    elif intent == 'GetIntent':
        message = __get(agency, city_full, param, user)
    else:
        raise Exception('Intent %s not found.' % intent)

    log.info('Response message = %s', message)
    return generate_response(message)


def get_default_params(city, request):
    city_full = city_constants[city]['full_name']
    request_json = request.get_json()
    log.info(request_json)
    result = request_json['result']
    original_request = request_json['originalRequest']

    try:
        log.info(original_request['data']['inputs'][0]['rawInputs'][0]['query'])
    except Exception:
        pass

    user = original_request['data']['user']['userId']
    intent = result['metadata']['intentName']
    param = result['parameters']
    agency = param['agency']
    return agency, city_full, intent, param, user


def __get(agency, city_full, param, user):
    preset = param['preset']
    return GetIntent.get(user, preset, agency, city_full)


def __set(agency, city_full, param, user):
    route = param['route']
    stop = param['stop']
    preset = param['preset']
    return SetIntent.add(user, route, stop, preset, agency, city_full)


def __check(agency, city_full, param):
    route = param['route']
    stop = param['stop']
    return CheckIntent.check(route, stop, agency, city_full)


def generate_response(message):
    return jsonify({
        "speech": remove_html(message),
        "displayText": remove_html(message)
    })


def remove_html(text):
    text = re.sub(r'<[^<]*?>', '', text)
    text = re.sub(r'\\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
