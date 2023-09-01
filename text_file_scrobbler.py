""" THIS SCRIPT DOESN'T UPLOAD YOUR SCROBBLES TO LAST.FM DIRECTLY
you will need to give the JSON output to Scrubbler WPF to upload your scrobbles.   
https://github.com/SHOEGAZEssb/Last.fm-Scrubbler-WPF
it's intended to make it easier to record your scrobbles manually in a text file then convert it to a format that Scrubbler WPF can understand
can also be useful for pasting text tracklists from online

we may add support for direct uploading in future however this was made by me (april) a few months before i realised how easy it was to get an API key

this hasn't been tested beyond my personal use of it, the implementation is flimsy and there isn't really any input validation.

--- ARGUMENTS ---

--file: the name of your input file (NOT INCLUDING EXTENSION). only .txt files are accepted, and the output is always the same filename with the .json extension

--mode: the method used for treating input
    default: every scrobble must have a time specified or implied (see FOLLOWTHROUGHS)
    mix:
        for contiguous mixes and playlists. only one start time is specified, the first scrobble is added at this start time and then the duration for each track is added on to a running total to find the other scrobble times.
        this was intended to be easy to copy and paste from a youtube video description or something like that
        i may add another version of this where the timestamps are the time since the start of the mix, not the individual durations of each track, since the descriptions of some mixes are like that

--start: the start time (used for mix mode

--debug: dumps some stuff to console, might not be comprehensive

--format_string: specifies where the parser should look for fields in each line of your input file. put field names in curly braces {}. available field names:
    artist
    track
    album
    duration (in mm:ss format (leading zeros not required)
    date
    time

--- INPUT FORMATTING ---

this script accepts .txt input with each line in the following formats (unless customised, see above)

    UNTIMED:
    mm:ss artist - track - album
        example: 6:12 Daft Punk - Fresh - Homework
    where mm:ss is the track duration (leading zeros not required)
    album is optional
    you'd use this for scrobbling tracks in series from a start time specified in the arguments.

    TIMED:
    YYYY-MM-DD HH:MM mm:ss artist - track - album
        example: 2023-08-06 21:50 4:04 Krome and Time - The Slammer

    FOLLOWTHROUGHS:
    in timed input files, you can start a line with "f" to use the time of the last scrobble + the duration of the track instead of typing a date and time again

    REPEATS:
    for repeated tracks or artists, you can replace a field with "s" to "inherit" the value of the field from the last line. in a repeated track you'll need to do this for duration, artist, track name and album if provided.

"""

import argparse
import json
import re
import string
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("--format_string", type=str)
parser.add_argument("--file", type=str)
parser.add_argument("--mode", type=str)
parser.add_argument("--start", type=str)
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

def default_mode(scrobbles):
    parser_untimed = get_parser_untimed()
    parser_timed = get_parser_timed()

    scrobble_json_list = []
    artist, track, album = (None, None, None)

    for scrobble in scrobbles:
        if args.debug:        
            print(scrobble)
        scrobble_dict = {}
        if scrobble[0] == "f":
            fields = get_fields(scrobble[2:], parser_untimed)
            if not fields:
                print("Could not parse: " + scrobble)
                continue
            if fields["duration"] != "s":
                duration_str = fields["duration"]
                # ELSE KEEP THE SAME TO INHERIT FROM PREVIOUS
            duration_min = int(duration_str.split(":")[0])
            duration_sec = int(duration_str.split(":")[1])
            datetime_obj = datetime_obj + timedelta(minutes=duration_min, seconds=duration_sec)

        else:
            fields = get_fields(scrobble, parser_timed)

            # currently deprecated
            # if args.date:
            #     datetime_obj = datetime.strptime(args.date+" "+fields["time"], "%Y-%m-%d %H:%M")
            # else:
            #     datetime_obj = datetime.strptime(fields["date"]+" "+fields["time"], "%Y-%m-%d %H:%M")

            datetime_obj = datetime.strptime(fields["date"]+" "+fields["time"], "%Y-%m-%d %H:%M")
            if fields["duration"] != "s":
                duration_str = fields["duration"]
                # ELSE INHERIT FROM PREVIOUS  
        
        # IF THE FIELD IS "S" THEN INHERIT FROM PREVIOUS
        if fields["artist"] != "s":
            artist = fields["artist"]
        if fields["track"] != "s":
            track = fields["track"]
        if fields.get("album", None) != "s":
            album = fields.get("album", None)

        scrobble_dict["ts"] = datetime_obj.strftime("%m/%d/%Y %H:%M")
        scrobble_dict["duration"] = "0:"+duration_str
        scrobble_dict["artist"] = artist
        scrobble_dict["track"] = track
        if album:
            scrobble_dict["album"] = album

        if args.debug:
            print(scrobble_dict)
        scrobble_json_list.insert(0, scrobble_dict)
    return scrobble_json_list
    
def mix_mode(scrobbles, start_time_str):
    start = 

    format_string = args.format_string
    if not format_string:
        format_string = "{position} {artist} - {track}"
    
    formatter = string.Formatter()
    parser = list(formatter.parse(format_string))

    prev_pos = ()
    scrobble_json_list = []
    pos_list = []

    counter = 0
    len_scrobbles = len(scrobbles)

    for scrobble in scrobbles:
        if args.debug:
            print(scrobble)
        scrobble_dict = {}

        fields = get_fields(scrobble, parser)
        if not fields:
            print("Could not parse: " + scrobble)
            continue

        pos_str = fields["position"]
        pos = (int(pos_str.split(":")[0]), int(pos_str.split(":")[1]))
        pos_list.append(pos)

        # ensures that the loop breaks before "pos end - end" in tracklist
        if counter == len_scrobbles-1:
            break
        counter += 1
        
        ts_int = int(start) + (pos[0]*60 + pos[1])
        scrobble_dict["ts"] = datetime.fromtimestamp(ts_int).strftime("%m/%d/%Y %H:%M")

        # IF THE FIELD IS "S" THEN INHERIT FROM PREVIOUS
        if fields["artist"] != "s":
            artist = fields["artist"]
        if fields["track"] != "s":
            track = fields["track"]
        if fields.get("album", None) != "s":
            album = fields.get("album", None)

        scrobble_dict["artist"] = artist
        scrobble_dict["track"] = track
        if album:
            scrobble_dict["album"] = album
        if args.debug:
            print(scrobble_dict)
        scrobble_json_list.insert(0, scrobble_dict)

    for index in range(len(scrobble_json_list)-1):
        pos = pos_list[index]
        next_pos = pos_list[index+1]
        duration_int = (next_pos[0]*60 + next_pos[1]) - (pos[0]*60 - pos[1])
        scrobble_json_list[index]["duration"] = f"0:{str(duration_int//60).zfill(2)}:{str(duration_int%60).zfill(2)}"

    return scrobble_json_list

def get_parser_untimed():
    format_string = args.format_string
    if not format_string:
        format_string = "{duration} {artist} - {track} - {album}"

    formatter = string.Formatter()
    parser = formatter.parse(format_string)
    return list(parser)
    
def get_parser_timed():
    # currently deprecated
    # if args.date:
    #     format_string = "{time} {duration} {artist} - {track} - {album}"
    # else:
    #     format_string = "{date} {time} {duration} {artist} - {track} - {album}"

    format_string = "{date} {time} {duration} {artist} - {track} - {album}"
    formatter = string.Formatter()
    parser = formatter.parse(format_string)
    return list(parser)

def get_fields(scrobble, parsed):
    fields = {}
    # print(parsed)
    for index in range(len(parsed) - 1):
        match = re.search(re.escape(parsed[index+1][0]), scrobble)
        # span = match.span()
        if match:
            span = match.span()
        else:
            # print(f"Couldn't find {parsed[index+1][1]} in {scrobble}")
            fields[parsed[index][1]] = scrobble
            if args.debug:
                print(fields)
            return fields
        
        fields[parsed[index][1]] = scrobble[:span[0]]
        scrobble = scrobble[span[1]:]

    if parsed[-1][1]:
        fields[parsed[-1][1]] = scrobble
    if args.debug:
        print(fields)
    return fields

def main():
    if args.file:
        file_name = args.file
    else:
        file_name = "scrobbles"

    with open(file_name+".txt", "r", encoding="utf-8") as file:
        scrobbles = file.readlines()
        scrobbles = [scrobble.rstrip() for scrobble in scrobbles]
    
    if args.start:
        start_ts = datetime.fromisoformat(args.start).timestamp()
    if args.mode == "mix":
        scrobble_json_list = mix_mode(scrobbles, start_time_str)
    else:
        scrobble_json_list = default_mode(scrobbles)

    with open(file_name+".json", "w", encoding="utf-8", errors="replace") as file:
        json.dump(scrobble_json_list, file)

if __name__ == "__main__":
    main()
