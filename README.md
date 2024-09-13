# UoA-Sentiment-Analysis

[Link to Websit](https://derekwong.shinyapps.io/individual_project/)

## Introduction: 
A Shiny App takes the sentimental score of all University-of-Auckland-related Reddit posts and compares the distribution of sentimental scores across different disciplines or faculties with respect to the user's choice.

## Python Script:
1. Activates the Reddit API `praw`.
2. Scrapes all the posts with the Subreddit of `R/universityofauckland`.
3. Look for the disciplines mentioned and assign the faculties respectively.
4. Assign general as disciplines and faculty for each post to allow comparison with the general trends.
5. Export the data frame as CSV.

## R Script:
1. Read in the CSV created previously.
2. Clean the data and separate each post into rows with respect to each discipline mentioned.
3. Activate the Shiny app.

## Shiny App:
1. Take in user's choice between comparing across disciplines or faculties.
2. Take in user's choice of interested fields to compare.
3. Create a box-and-whisker plot accordingly.
