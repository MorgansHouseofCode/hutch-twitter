#!/usr/bin/python

# instead this will be converted to a JSON file which can then be edited 
# similarly to the other one

import sys
import csv
from datetime import datetime
import json

with open("UserTimeLine_20170714_121306.txt", "r") as user_timeline_file:
    user_timeline_file_text = user_timeline_file.read()

main_data = []

for i, line in enumerate(user_timeline_file_text.split("\n")):
    line_split = line.split("\t")
    main_data.append({
        "username" : line_split[1].lower(),
        "id" : line_split[2], 
        "date" : line_split[3], 
        "text" : line_split[4], 
        "favorites" : line_split[5], 
        "retweets" : line_split[6], 
        "mentions" : line_split[7], 
        "hashtags" : line_split[8], 
        "geo" : line_split[9]
    })

tweetsJson = json.dumps(main_data, separators=(',',':'))
text_file = open("usertimeline.json", "w")
text_file.write(tweetsJson)
text_file.close()
