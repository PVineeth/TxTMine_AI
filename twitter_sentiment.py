from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from sklearn.model_selection import train_test_split
import csv
from modules import CSVWriter

analyser = SentimentIntensityAnalyzer()
tweets = list()
sentiTweets = list()
csvwr = CSVWriter.CSVWriter('CSV/tweets_sentiment.csv')

def sentiment_analyzer_scores(sentence):
	score = analyser.polarity_scores(sentence)
	# Delete 'compound' Key
	try:
		del score['pos']
		del score['neu']
		del score['neg']
	except KeyError:
		pass

	if score['compound'] >= 0.05:
		sentiment = "positive"
	elif score['compound'] > -0.05 and score['compound'] < 0.05:
		sentiment = "neutral"
	elif score['compound'] <= -0.05:
		sentiment = "negative"

	# if sentiment == "negative":
	# print(sentence, "\t:::::\t", sentiment, "\n\n")
	sentiTweets.append((sentence,sentiment))
	csvwr.write((sentence, sentiment))
	# if (score['neu'] ==  1.0):
	#     print("\t", str(score), "   ", sentence, "\n")

def assignSentiment():
	print('Assigning Sentiments.\n')
	csvwr.writeHeader(('Tweets','Sentiment'))
	for tweet in tweets:
		sentiment_analyzer_scores(tweet[0])
	#print("\nLength of Tweets List:", len(tweets))

def readCSV(fileName):
	print("\nReading CSV.\n")
	global tweets
	with open(fileName,'rt') as f:
		data = csv.reader(f)
		for row in data:
				tweets.append(row)

def splitData():
	print("Splitting data.")
	df = pd.DataFrame(sentiTweets)
	# Train = 0.8, Test = 0.2
	xTrain, xTest = train_test_split(df, test_size = 0.2, random_state = 0)
	xTrain.columns = ["Tweet", "Sentiment"]
	xTest.columns = ["Tweet", "Sentiment"]
	xTrain.to_csv("CSV/trainData.csv", sep='\t', encoding='utf-8', index=False)
	xTest.to_csv("CSV/testData.csv", sep='\t', encoding='utf-8', index=False)
	print("\nDone Splitting Data!\n")


readCSV("Twitter_Data/tweets.csv")
assignSentiment()
splitData()
csvwr.close()