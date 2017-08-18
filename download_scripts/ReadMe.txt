HOW THE DATA WAS DOWNLOADED AND COLLECTED AND FORMATTED

Koustuv gave me UserTimeline txt file with tab-separated data

formatusertimeline.py converted plaintext to JSON data, usertimeline.json

sanitizefile.py fixed the formatting issues in the "text" field of the data Koustuv sent me, with links being broken and text formatting being weirdly misrepresented due to the web scraper's interpretation of the Twitter website's HTML

sanitize_user_timeline.py unshortened URLs, added additional info as to whether a tweet contained photos or links, whether a URL was shortened with a shortening service, and performed a couple other formatting issues

addurlcolumns.py added an additional data point, the text field but removed of any URLs (so the text would be easier to classify and interpret with NLP)

addfavorites.py added the Twitter user ID numbers of users that favorited the tweets in our database

addretweets.py added the data available on how the tweets in our @fredhutch database were retweeted - specifically, who retweeted the tweet and when they did it.

combineretweetsandfavorites.py was a custom script built after I realized I had two separate tweet database files - one with the favoriting users and one with the retweets - and needed to combine the two into a master database. 

addsentimentdata.py utilized the Google Cloud Platform to assign a "sentiment" value for each tweet, ranging from -1.0 to +1.0, that evoked how "negative" or "positive" a tweet was.

This completed the list of scripts that were used, in sequence, to develop the tweet database that is the end result of these scripts being run.
