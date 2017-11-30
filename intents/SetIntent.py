from flask import render_template
import RestTemplate
import logging as log


def add(user, route, stop, preset, agency, city_full):
    log.info('User=%s, Route=%s, Stop=%s, Preset=%s, Agency=%s, City=%s', user, route, stop, preset, agency, city_full)
    city_agency = '%s-%s' % (city_full.lower().replace(' ', ''), agency.replace(' ', '-'))
    response = __get_response(user, route, stop, preset, city_agency)
    if response.status_code != 200:
        log.error(response.text)
        return render_template('internal_error_message')
    return render_template('set_success_message', route=route, stop=stop, preset=preset,
                           agency='%s %s' % (city_full, agency))


def __get_response(user, route, stop, preset, city_agency):
    parameters = {
        'user': user,
        'route': route,
        'stop': stop,
        'preset': preset,
        'agency': city_agency
    }
    return RestTemplate.get_response('add', parameters)
