# Returns how many of a user's top 100 artists are in the site's top 500 artists
# Usage: python mainstream.py user --period (7day|1month|3month|6month|12month|alltime) --userartists (int) --chartartists (int)
# Defaults to alltime period, 100 user artists, 500 chart artists.

import argparse
import requests
from lastfm-api import API_KEY

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("Argument must be a positive int!")
    return ivalue

argparser = argparse.ArgumentParser(description="Returns how many of a user's top artists are in the top 1000 artists.", epilog="Written by @duh as part of lastfm-utils.")
argparser.add_argument("username", type=str)
argparser.add_argument("--period", type=str, choices=["7day", "1month", "3month", "6month", "12month", "overall"], help="The time period to retrieve the user's top artists from.", required=False, default="at")
argparser.add_argument("--userartists", type=check_positive, help="The amount of top artists to retrieve for the user.", required=False, default=100)
argparser.add_argument("--chartartists", type=check_positive, help="The amount of top artists to retrieve from the charts.", required=False, default=500)

args = argparser.parse_args()

chart_response = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={API_KEY}&format=json&limit={args.chartartists}")
user_response = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={args.username}&api_key={API_KEY}&format=json&limit={args.userartists}&period={args.period}")
chart_response.raise_for_status()
user_response.raise_for_status()

top_artists = set()
user_top_artists = set()
listeners_dict = {}

for top_artist in chart_response.json()["artists"]["artist"]:
    top_artists.add(top_artist["name"])
    listeners_dict[top_artist["name"]] = top_artist["listeners"]
    
for top_artist in user_response.json()["topartists"]["artist"]:
    user_top_artists.add(top_artist["name"])
    
intersection_sorted = sorted(list(top_artists.intersection(user_top_artists)), key=lambda artist: listeners_dict[artist], reverse=True)
print(listeners_dict)

if(len(user_top_artists) < args.userartists):
    print(f"User does not have enough artist scrobbles in this period! ({len(user_top_artists)} artists, {args.userartists} required)")
else:
    print(f"Mainstream artists: {intersection_sorted}\n\n{len(top_artists.intersection(user_top_artists))} ({round((len(top_artists.intersection(user_top_artists)) / args.userartists) * 100, 2)}%) of {args.username}'s top {args.userartists} artists are in the top {args.chartartists} charts.")
