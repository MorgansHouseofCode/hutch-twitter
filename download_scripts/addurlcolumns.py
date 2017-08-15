#!/usr/bin/python

import sys
import json
import httplib
import urlparse

# this script takes a url-containing json file as input and produces a 
# formatted json file that strips the url from the "text" property and 
# creates 4 new columns:
#   -"original_url" which contains the stripped url from text
#   -"fixed_url" which contains an unshortened link if the "full_url" 
#   is a shortened link from bit.ly or something like that
#   -boolean value "link_shortened" which is TRUE if a link-shortening 
#   service was used, FALSE if not
#   -boolean value "contains_link" which is TRUE if there is even a 
#   link at all, and FALSE if not (and thus none of the previous stuff 
#   even had to happen)
#   -"text_no_url" which contains the text without "pic.twitter" or 
#   "http" urls

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

input_filename = sys.argv[1]

with open(input_filename) as input_file:
    input_data = json.load(input_file)

for i, tweet in enumerate(input_data):
    # First, check if there even is a link
    contains_link = False
    original_url = ""
    fixed_url = ""
    text_no_url = tweet["text"]
    link_shortened = False
    split_text = tweet["text"].split()
    for k, word in enumerate(split_text):
        if word[:4] == "http":
            # We found a link
            contains_link = True
            original_url = word
            # Fix weird ... issue with unshortened links
            should_be_clipped = False
            if original_url[-1:] == u"\u2026":
                should_be_clipped = True
            if should_be_clipped:
                original_url = original_url[:-1]
    # If we found a link, proceed with the next section
    if contains_link:
        # Test if the link should be unshortened
        if (("bit.ly" in original_url) or
        ("goo.gl" in original_url) or 
        ("is.gd" in original_url) or 
        ("ow.ly" in original_url) or 
        ("t.co" in original_url) or 
        ("tinyurl.com" in original_url) or 
        ("youtu.be" in original_url)):
            # Unshorten the URL
            fixed_url = unshorten_url(original_url.encode("ascii", "ignore"))
            if fixed_url != original_url:
                link_shortened = True
            else:
                fixed_url = ""
    # Remove pic.twitter links and http links from text to create a NLP
    # working variant of the original text
    split_text = text_no_url.split()
    text_no_url = ""
    for k, word in enumerate(split_text):
        # Test if word starts with http or pic.twitter.com
        if not ( (word[:4] == "http") or (word[:15] == "pic.twitter.com") ):
            text_no_url = text_no_url + word + " "
    text_no_url = text_no_url[0:len(text_no_url) - 1]
    # Finally, push this information to the main data object
    input_data[i]["contains_link"] = contains_link
    input_data[i]["original_url"] = original_url
    input_data[i]["fixed_url"] = fixed_url
    input_data[i]["link_shortened"] = link_shortened
    input_data[i]["text_no_url"] = text_no_url

final_json = json.dumps(input_data, separators=(",",":"))
final_file = open(input_filename[:-5] + "_with_new_columns.json", "w")
final_file.write(final_json)
final_file.close()
