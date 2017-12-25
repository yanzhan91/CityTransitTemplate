from flask import Flask, request as flask_request
from flask_ask import Ask, context, request as ask_request

import Alexa

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def launch():
    city = flask_request.args.get('city')
    return Alexa.launch_intent(city)


@ask.intent('AMAZON.HelpIntent')
def help_intent():
    city = flask_request.args.get('city')
    return Alexa.help_intent(city)


@ask.intent('AMAZON.StopIntent')
def stop_intent():
    return Alexa.stop_intent()


@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    return Alexa.stop_intent()


@ask.intent('CheckIntent')
def check_intent(route, stop, agency):
    city = flask_request.args.get('city')
    return Alexa.check_intent(ask_request, city, route, stop, agency)


@ask.intent('SetIntent')
def set_intent(route, stop, preset, agency):
    city = flask_request.args.get('city')
    user = context.System.user.userId
    return Alexa.set_intent(ask_request, city, user, route, stop, preset, agency)


@ask.intent('GetIntent')
def get_intent(preset, agency):
    city = flask_request.args.get('city')
    user = context.System.user.userId
    return Alexa.get_intent(ask_request, city, user, preset, agency)

if __name__ == '__main__':
    app.config['ASK_VERIFY_REQUESTS'] = False
    app.run()
