# Estimates how long it will take a Last.fm user to reach a specified number of scrobbles.
# Usage: python pace.py user number

import argparse
from datetime import date
from fmapi import get_request, check_positive
import math
import requests


argparser = argparse.ArgumentParser(description="Estimates how long it will take a Last.fm user to reach a specified number of scrobbles.", epilog="Written by @duh as part of lastfm-utils.")
argparser.add_argument('username', type=str)
argparser.add_argument('milestone', type=check_positive)
args = argparser.parse_args()

response = get_request({
    "method": "user.getinfo",
    "user": args.username
})
    
scrobbles = int(response.json()["user"]["playcount"])
registered = date.fromtimestamp(response.json()["user"]["registered"]["#text"])
age = (date.today() - registered).days
average = scrobbles / age

if args.milestone > scrobbles:
    milestonedays = math.ceil((args.milestone - scrobbles) / average)
    print(f"Based on an average of {average} scrobbles per day, {args.username} is likely to reach {args.milestone} scrobbles in {milestonedays} days.")
else:
    print(f"{args.username} has already reached {args.milestone} scrobbles!")