#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys
import os
import json

input_filename = sys.argv[1]

with open(input_filename) as json_file:
    data = json.load(json_file)

# "data" is a python object with our JSON data loaded

for iter, tweet in enumerate(data):
    text = tweet["text"]
    split_text = text.split()
    # The splicing is accomplished with an array of booleans corresponding
    # to the split chunks from "text.split()". If the boolean is true then 
    # a space should follow the chunk in the final string, if the boolean is 
    # not true then a space should not follow the chunk in the final string.
    space_follows_chunk = [True] * len(split_text)
    if len(space_follows_chunk) > 0:
        space_follows_chunk[len(space_follows_chunk) - 1] = False
        for index, text_chunk in enumerate(split_text):
            if text_chunk.find("http") == 0 and index + 1 < len(split_text):
                # A url was found in the text
                # Get next chunk after this one:
                next_chunk = split_text[index + 1]
                # Splice the next_chunk and the current chunk together
                space_follows_chunk[index] = False
                # Now test to see if chunk "index + 2" exists; if so 
                # then test it for splicing as well
                if index + 2 < len(split_text):
                    chunk_after_next = split_text[index + 2]
                    if not ( chunk_after_next.find("#") == 0 or
                        chunk_after_next.find("@") == 0 or
                        chunk_after_next.find("\u2026") == 0 or
                        chunk_after_next.find("http") == 0 or
                        chunk_after_next.find("pic.twitter.com") == 0 ):
                        space_follows_chunk[index + 1] = False
        # Now that space_follows_chunk is organized we can create our final string
        final_text = ""
        for index, chunk in enumerate(split_text):
            final_text = final_text + chunk
            if space_follows_chunk[index]:
                final_text = final_text + " "
        if final_text[len(final_text) - 2:len(final_text)] == u" \u2026":
            final_text = final_text[0:len(final_text) - 2]
        data[iter]["text"] = final_text

finalJSON = json.dumps(data, separators=(',',':'))
finalFile = open(input_filename[:-5] + "_sanitized.json", "w")
finalFile.write(finalJSON)
finalFile.close()