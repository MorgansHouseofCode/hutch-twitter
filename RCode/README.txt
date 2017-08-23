This Folder holds all the R code that was used in the project.

All code is commented through out the code this section will be sued to explain what the code is and what we used it for.

We did LDA (latent Dirichlet allocation) to create general topics for all the tweets but found that was not productive to our ends.  Instead we employed a Supervised Random Forest to label our data.  

We kept the LDA code because we were able to find the frequency of each word and able to create some intresting visulations in the code.  For example we are able to create a word cloud for our data.

We used linear regression to predict how well a tweet will do.  In the Predictive Analysis we also found which characteristics are the most important in predicting tweets and likes 

2yearstweetstfdf ended up not being used soley to fidn the most common words in the corpus is and then use those words to enhance the stop word dictionary in Hutch LDA

Networkgraph uses Twitter API to gather data about Hutch's followers and see which of the top active users on Hutch's twitter channel have common followers.

