"""Main module."""
#######################################################################
# indicative.py
# Standalone Client Library for Indicative's Input API.
# This client is SYNCHRONOUS. It's recommended that you use this client
# in the async processing part of your infrastructure.
# This client is a good choice for small volumes of events in standalone
# projects or for testing.
#######################################################################
from urllib.parse import urlparse
import http.client
import sys
import logging
import time
import json

API_URL = 'https://api.indicative.com/service'
CONTENT_TYPE = 'application/json'
LOGGER_NAME = __name__

_api_key = None
_initialized = False
_misconfigured_warning = False


def _sendEvent(event, path):
    try:
        url = urlparse(API_URL + '/' + path)
        conn = http.client.HTTPConnection(url.netloc)
        event_string = json.dumps(event)
        conn.request('POST', url.path, event_string, {'Content-Type':'application/json'})
        res = conn.getresponse()
        if res.status != 200:
            logging.getLogger(LOGGER_NAME).error(res.read())
    except:
        logging.getLogger(LOGGER_NAME).exception('Encountered exception while sending event.')


""" Sends an event to the Indicative API endpoint.
:param event_name: name of the event
:param event_unique_id: unique identifier for the user associated with the event
:param param_dict: dictionary object containing property names and values
:param api_key: the project's API key
"""
def record(event_name, event_unique_id, param_dict={}, api_key=None):
    global _initialized
    global _misconfigured_warning
    global _shutdown
    global _api_key
    if api_key == None:
        if _api_key == None:
            if _misconfigured_warning:
                return
            logging.getLogger(LOGGER_NAME).error('record() called before init() is called! '+
                                                                                    'Please call init() first. This message '+
                                                                                    'will only be logged once.')
            _misconfigured_warning = True
            return
        api_key = _api_key
    else:
        if not _initialized:
            init(api_key)


    event = {'eventName':event_name, 'apiKey':api_key, 'eventUniqueId':event_unique_id,
            'eventTime':int(round(time.time()*1000)), 'properties': param_dict}
    _sendEvent(event, 'event')



""" Identify a user to the Indicative API endpoint.
:param unique_id: unique identifier for the user
:param properties: user properties
:param api_key: the project's API key
"""
def identify(unique_id, param_dict={}, api_key=None):
    global _initialized
    global _misconfigured_warning
    global _shutdown
    global _api_key
    if api_key == None:
        if _api_key == None:
            if _misconfigured_warning:
                return
            logging.getLogger(LOGGER_NAME).error('record() called before init() is called! '+
                                                    'Please call init() first. This message '+
                                                    'will only be logged once.')
            _misconfigured_warning = True
            return
        api_key = _api_key
    else:
        if not _initialized:
            init(api_key)


    event = {'apiKey':api_key, 'uniqueId':unique_id,
            'properties': param_dict}
    _sendEvent(event, 'identify')

""" Sets the API key and number of threads to use when recording events.
:param api_key: the project's API key
:param num_threads: the number of threads to use
"""
def init(api_key):
        global _initialized
        global _api_key
        _initialized = True
        _api_key = api_key
