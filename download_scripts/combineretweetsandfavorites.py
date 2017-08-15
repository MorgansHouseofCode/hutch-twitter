#!/usr/bin/python

import __future__
import sys
import json

input_retweets_filename = sys.argv[1]
input_favorites_filename = sys.argv[2]

with open(input_retweets_filename) as input_retweets_file:
    input_retweets_data = json.load(input_retweets_file)

with open(input_favorites_filename) as input_favorites_file:
    input_favorites_data = json.load(input_favorites_file)

output_data = input_retweets_data

for index, tweet in enumerate(output_data):
    output_data[index]["favorites"] = \
        str(input_favorites_data[index]["favorites"])
    if "favoriting_users" in input_favorites_data[index]:
        output_data[index]["favoriting_users"] = \
            input_favorites_data[index]["favoriting_users"]

output_data_json_string = json.dumps(output_data, separators=(',',':'))
output_file = open("user_timeline_with_favorites_and_retweets.json", "w")
output_file.write(output_data_json_string)
output_file.close()