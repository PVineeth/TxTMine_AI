from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from modules import CSVWriter

analyser = SentimentIntensityAnalyzer()
tweets = list()
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
	csvwr.write((sentence, sentiment))
	# if (score['neu'] ==  1.0):
	#     print("\t", str(score), "   ", sentence, "\n")

def assignSentiment():
	print('Assigning Sentiments\n')
	csvwr.writeHeader(('Tweets','Sentiment'))
	for tweet in tweets:
		sentiment_analyzer_scores(tweet[0])
	#print("\nLength of Tweets List:", len(tweets))

def readCSV():
	print("\nReading CSV...\n")
	global tweets
	with open("Twitter_Data/tweets.csv",'rt') as f:
		data = csv.reader(f)
		for row in data:
				tweets.append(row)


readCSV()
assignSentiment()
csvwr.close()