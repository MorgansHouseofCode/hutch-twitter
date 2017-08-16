PROCEDURE OF SUPERVISED CLASSIFICATION

Manual Classifiers REDUX new columns.xlsx has 1400 tweets manually classified in 10 classifiers for types of tweets.
Tweets have been classified in a random order, using the Excel RAND() function.
Columns have been added for stop words, showing count of each of them per tweet.
Some science/Hutch related stop words have been added such as "study" and "cancer".

Supervised Random Forest.rmd inputs the file and runs its algorithms to show delineations between categories based on stop word usage.
Data frame is split into classified ("train") and unclassified data ("test").
Code runs model on classified data.
Code prints out the mean decrease in average for certain stop words to show the best words to separate classifiers.
Code uses "predict" function to classify all the unclassified tweets, and print them into the "test" data frame.
New data frame created with original "train" and updated "test".
New data frame printed into a csv file format called Full Classifiers V4.csv.

Full Classifiers V4.csv run through Power Query and saved as Full Classifiers V4 FIXED.xlsx.
Power Query was done in order to make the data easier to manipulate.
One manipulation was done to add the Tweet ID to the file by drawing from the original data frame.
