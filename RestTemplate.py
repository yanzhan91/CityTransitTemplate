from Constants import city_constants
import requests
import logging as log


def get_response(path, parameters):
    url = '%s/%s' % (city_constants['eztransit_url'], path)
    log.info('Api_url=%s', url)
    return requests.get(url, params=parameters)


def post_response(path, parameters):
    url = '%s/%s' % (city_constants['eztransit_url'], path)
    log.info('Api_url=%s', url)
    return requests.post(url, data=parameters)
