# Methods for working with the Last.fm API. Do not touch this file unless you know what you are doing!
import requests
import argparse
from fmcreds import API_KEY, USER_AGENT

# Validation methods
def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("Argument must be a positive int!")
    return ivalue

# API methods
def get_request(payload):
    payload["api_key"] = API_KEY
    payload["format"] = "json"
    
    response = requests.get("https://ws.audioscrobbler.com/2.0/", headers={"user-agent": USER_AGENT}, params=payload)
    response.raise_for_status()
    return response
