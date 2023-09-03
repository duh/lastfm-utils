# lastfm-utils
Collection of Python programs for analysing Last.fm data maintained by [@duh](https://www.github.com/duh) and [@apr1lfm](https://www.github.com/apr1lfm). You are free to use these in your own projects - credit would be appreciated!

## How do I use these?
You must have a Last.fm API key to use these programs. You can apply for one [here](https://www.last.fm/api/account/create). 
<br>The **FMapi.py** file contains key functions, and must also be downloaded and placed in the same directory as any saved scripts.
<br>The Python `requests` module is also required for most of these scripts. You can install it from the terminal using `pip install requests`
<br><br>An **FMcreds.py** file must be created in the same directory with the following content:
```py
API_KEY = " " # Your API key goes here.
USER_AGENT = "LastFM-Utils script" # This can be changed, but please abide by Last.fm TOS: "Please use an identifiable User-Agent header on all requests. This helps our logging and reduces the risk of you getting banned."
```

## ⚠ Disclaimer
You are responsible for your use of these programs, and must follow the [API Terms of Service](https://www.last.fm/api/tos)

![Last.fm logo being hit with a hammer and smashing](https://github.com/duh/lastfm-utils/blob/main/img/lastfm-utils.png)
