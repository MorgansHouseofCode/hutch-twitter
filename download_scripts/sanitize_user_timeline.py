#!/usr/bin/python

import sys
import csv
from datetime import datetime
import json
import httplib
import urlparse

def unshorten_url(url):
    try:
        parsed = urlparse.urlparse(url)
        h = httplib.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status/100 == 3 and response.getheader('Location'):
            return response.getheader('Location')
        else:
            return url
    except:
        return url

with open(sys.argv[1], 'r') as myfile:
  data=json.load(myfile)

for tweet in data:
    tweet["text"] = tweet["text"].replace(unichr(160), " ")
    tweet["text"] = tweet["text"].replace("http", " http")
    tweet["text"] = tweet["text"].replace("pic.twitter.com", " pic.twitter.com")
    new_text = ""
    new_text_filtered = ""
    for word in tweet["text"].split():
        new_text = new_text + word + " "
        if not (("http" in word) or ("pic.twitter.com" in word)):
            new_text_filtered = new_text_filtered + word + " "
    new_text = new_text[0:len(new_text) - 1]
    new_text_filtered = new_text_filtered[0:len(new_text_filtered) - 1]
    tweet["text_filtered"] = new_text_filtered
    tweet["text"] = new_text
    if "pic.twitter.com" in tweet["text"]:
        tweet["has_picture"] = True
    else:
        tweet["has_picture"] = False
    if "http" in tweet["text"]:
        tweet["has_link"] = True
    else:
        tweet["has_link"] = False
    if tweet["has_link"]:
        for word in tweet["text"].split():
            if "http" in word:
                # We found our link word
                tweet["original_url"] = word
                original_url = tweet["original_url"]
                # Now check if the URL was shortened
                url_shortened = False
                fixed_url = ""
                if (("://bit.ly" in original_url) or
                ("://goo.gl" in original_url) or 
                ("://is.gd" in original_url) or 
                ("://ow.ly" in original_url) or 
                ("://t.co" in original_url) or 
                ("://tinyurl.com" in original_url) or 
                ("://youtu.be" in original_url)):
                    # Unshorten the URL
                    print(original_url)
                    fixed_url = unshorten_url(original_url.encode("ascii", "ignore"))
                    if fixed_url != original_url:
                        url_shortened = True
                    else:
                        fixed_url = ""
                tweet["fixed_url"] = fixed_url
                tweet["url_shortened"] = url_shortened
    else:
        tweet["original_url"] = ""
        tweet["url_shortened"] = None
        tweet["fixed_url"] = ""

tweetsJson = json.dumps(data, separators=(',',':'))
text_file = open("user_timeline_sanitized.json", "w")
text_file.write(tweetsJson)
text_file.close()