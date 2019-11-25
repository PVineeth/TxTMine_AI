#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import necessary modules
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

initFolder = "PDFs/"
folders = list()
fileNames = list()


def getFolders():
	global folders
	folders = os.listdir(initFolder)
	folders.remove('.DS_Store')

def getFiles(folderName):
	global fileNames
	fileNames = os.listdir(initFolder+folderName)
	try:
		fileNames.remove('.DS_Store')
	except:
		pass

def pdfToText(folderName, fileName):
	fname = initFolder + folderName + '/' + fileName 
	#print("\r : " + filename) # DEBUG LINE
	#open allows you to read the file
	pdfFileObj = open(fname,'rb')
	#The pdfReader variable is a readable object that will be parsed
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	#discerning the number of pages will allow us to parse through all #the pages
	try:
		num_pages = pdfReader.numPages
		count = 0
		text = ""
		#The while loop will read each page
		while count < num_pages:
		    pageObj = pdfReader.getPage(count)
		    count +=1
		    text += pageObj.extractText()
		#This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
		if text != "":
		   text = text
		#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
		else:
			print("Ignoring: " + fname)
			pass
		   #text = textract.process(fname, method='tesseract', language='eng')
		# Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
		# Now, we will clean our text variable, and return it as a list of keywords.

		# print(text + "\n\n\n") # DEBUG LINE

		# TxT to Keywords

		#The word_tokenize() function will break our text phrases into #individual words
		tokens = word_tokenize(text)
		#we'll create a new list which contains punctuation we wish to clean
		punctuations = ['(',')',';',':','[',']',',', '&','',' ', '  ','.','--','-',"``","`","~","''",'>','Ł',"'"]
		#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
		# stop_words = stopwords.words('english')
		# #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
		# keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

		keywords = [word for word in tokens if not word in punctuations]

		writeData(keywords)

		# if checkHexData(keywords) == 'accept':
		# 	writeData(keywords)
		print('Writing to Text File: ' + folderName + "/" + fileName)
		# else:
		# 	print('Ignoring: ' + folderName + "/" + fileName)

		# print(keywords) # DEBUG LINE
	except:
		pass

def writeData(keywordsData):

	#print(keywordsData)
	with open("News_Articles/NewsArticlesData.txt", "a") as txtFile:
		for data in keywordsData:
			string = data + "\n"
			txtFile.write(string)

def checkHexData(keywordsData):
	# If hex data count is more than 10 then ignore the file
	count = 0
	loopCounter = 0
	for data in keywordsData:
		loopCounter = loopCounter + 1
		if len(data) == 2:
			count = count + 1
			if loopCounter == 10:
				break

	if count >= 15:
		return 'ignore'
	else:
		return 'accept'

def checkFileExists(fileName):
	if os.path.isfile(fileName):
		os.remove(fileName)

# PROGRAM STARTS HERE
checkFileExists("News_Articles/NewsArticlesData.txt")
getFolders()

for folder in folders:
	#print(folder + "/")
	getFiles(folder)
	for file in fileNames:
		#print("\t" + file + "\r")
		pdfToText(folder,file)