# Returns mutual friends between two users
# Usage: python mutual-friends.py user1 user2

import argparse
import requests
from lastfm-api import API_KEY

def store_arg(value): # This is a really janky way to store the first argument as a variable so the program can make sure the same username has not been entered twice.
    global username1 
    username1 = str(value)
    return str(value)

def compare_arg(value):
    if str(value) == username1:
        raise argparse.ArgumentError("Usernames cannot be the same")
    return str(value)

argparser = argparse.ArgumentParser(description="Returns the mutual friends of two Last.fm users.", epilog="Written by @duh as part of lastfm-utils.")
argparser.add_argument('username1', type=store_arg)
argparser.add_argument('username2', type=compare_arg)
args = argparser.parse_args()

friends1 = set()
friends2 = set()

for user in args.username1, args.username2:
    response = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getfriends&user={user}&api_key={API_KEY}&format=json")
    response.raise_for_status() # End program if error occurs
    
    for record in response.json()["friends"]["user"]:
        if user == args.username1:
            friends1.add(record["name"])
        else:       
            friends2.add(record["name"])
            
if len(friends1.intersection(friends2)) == 0:
    print("No mutual friends!")
else:
    print(friends1.intersection(friends2))
        
