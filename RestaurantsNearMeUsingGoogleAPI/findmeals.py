"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
from json import loads
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# --------------- Helpers that build all of the responses ----------------------
OK_STATUS_CODE = 'OK'
ZERO_RESULTS_STATUS_CODE = 'ZERO_RESULTS'
NEARBY_PLACE_LIMIT = 5
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_test_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Test"
    places = get_nearby_places()
    result = ''
    for place in places:
        result += place + ', '
    speech_output = "The Top  Restaurant near by based on the user ratings are "+result
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_nearby_places():
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=29.4229629,-98.5029771&rankby=distance&type=restaurant&key=AIzaSyCzwnTnE1ZTYwn31SMA24xAS7iNjDN2BT4'

    response = loads(urlopen(Request(url)).read())
    print('response data',response)
    if response['status'] != OK_STATUS_CODE and response['status'] != ZERO_RESULTS_STATUS_CODE:
        raise HTTPError(response['status'])

    # Return the unique names of nearby places
    return list(set([place['name'] for place in response['results']]))

def get_phone_number(placename):
    print('the placename',placename)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=29.4229629,-98.5029771&rankby=distance&type=restaurant&key=AIzaSyCzwnTnE1ZTYwn31SMA24xAS7iNjDN2BT4'

    response = loads(urlopen(Request(url)).read())
    print('response data',response)
    if response['status'] != OK_STATUS_CODE and response['status'] != ZERO_RESULTS_STATUS_CODE:
        raise HTTPError(response['status'])

    # Return the unique names of nearby places
    results = response['results']
    print('results',results)
    placeid=''
    for result in results:
        print('result',result)
        rowvalue = result['name']
        print('rowvalue',rowvalue)
        if(rowvalue.lower() == placename.lower()):
            placeid = result['place_id']
    
    print('the place id is',placeid)
    url1 = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='+placeid+'&key=AIzaSyCzwnTnE1ZTYwn31SMA24xAS7iNjDN2BT4'
    response1 = loads(urlopen(Request(url1)).read())
    print('response data',response1)
    if response1['status'] != OK_STATUS_CODE and response1['status'] != ZERO_RESULTS_STATUS_CODE:
        raise HTTPError(response1['status'])

    # Return the unique names of nearby places
    print('result value',response1['result'])
    results1 = response1['result']
    phonenumber = results1['formatted_phone_number']
    print('results1',results1['formatted_phone_number'])
    return phonenumber

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Restaurant Application! We help you find restaurant near by and connect with them."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_callrestaurant_response(intent_request):
    
    session_attributes = {}
    card_title = "Welcome"
    speech_output=''
    intent = intent_request['intent']
    print('intent',intent)
    slots = intent['slots']
    print('slots',slots)
    #print('restaurant',intent_request['intent']['slots']['restaurant']['value'])
    for slot in slots:
        slot1 = slots[slot]
        print('slot1',slot1)
        print('slot1 keys',slot1.keys())
        if ('value' in slot1.keys()):
            phonenumber = get_phone_number(slot1['value'])
            speech_output = "For Placing order in Restaurant " + slot1['value'] + " . You can call phone number "+ phonenumber +" now."
        else:
            pass
        
    #speech_output = "We will call the restaurant now. Alexa, Call 2109659334."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "test":
        return get_test_response()
    elif intent_name == "callrestaurant":
        return get_callrestaurant_response(intent_request)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])