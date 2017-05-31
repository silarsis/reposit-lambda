#!/usr/bin/env python
" Handler for lambda behaviour "

import reposit

def build_speechlet_response(output, should_end_session):
    " Helper to build a speech response from a string "
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    " Helper to build a full response "
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def get_welcome_response():
    " Return a welcome for starting a session without asking for anything "
    session_attributes = {}
    speech_output = "Please ask me for the battery status"
    should_end_session = True
    return build_response(
        session_attributes, build_speechlet_response(speech_output, should_end_session))

def get_status_response():
    " Return a status "
    session_attributes = {}
    speech_output = reposit.status()
    should_end_session = True
    print(speech_output)
    return build_response(
        session_attributes, build_speechlet_response(speech_output, should_end_session))

def handle_session_end_request():
    " Ending the session quietly "
    should_end_session = True
    speech_output = None
    return build_response({}, build_speechlet_response(speech_output, should_end_session))

def on_intent(intent_request, session):
    " Execute an intent "
    print("on_intent requestId=" + intent_request['requestId'] \
        + ", sessionId=" + session['sessionId'])
    intent_name = intent_request['intent']['name']
    if intent_name == "status":
        return get_status_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_started(session_started_request, session):
    " Debug for session starting "
    print("on_session_started requestId=" + session_started_request['requestId'] \
        + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    " Debug for launch "
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" \
        + session['sessionId'])
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
    " Debug for session ending "
    print("on_session_ended requestId=" + session_ended_request['requestId'] \
        + ", sessionId=" + session['sessionId'])

def lambda_handler(event, _context):
    " Handler for lambda usage "
    print("event.session.application.applicationId=" \
        + event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
