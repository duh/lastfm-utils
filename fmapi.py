# Defines variables and methods for working with the Last.fm API
import requests
import argparse

API_KEY = " " # Your API key goes here.
USER_AGENT = "LastFM-Utils script" # This can be changed, but please abide by Last.fm TOS: "Please use an identifiable User-Agent header on all requests. This helps our logging and reduces the risk of you getting banned."

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("Argument must be a positive int!")
    return ivalue

def get_request(payload):
    payload["api_key"] = API_KEY
    payload["format"] = "json"
    
    response = requests.get("https://ws.audioscrobbler.com/2.0/", headers={"user-agent": USER_AGENT}, params=payload)
    response.raise_for_status()
    return response
