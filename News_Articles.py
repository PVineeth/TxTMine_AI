#!/usr/bin/env python
# coding: utf-8

# Retrieving Data From Websites

# Using Azure/Bing Search API to retrieve articles

import requests
import os
import time
from weasyprint import HTML


search_term = ['AI', 'Impact Of AI', 'AI Risk','AI Future', 'futureofwork', 'SelfDrivingCars', 'AI Jobs', 'Artificial Intelligence Jobs', 'AIGovernance', 'machinelearning', 'AutonomousVehicles', 'DeepLearning']

subscription_key = "f1fc1b012f0b4f9fbb87ad0927eb3f5c"
search_url = "https://eastus.api.cognitive.microsoft.com/bing/v7.0/news/search"
no_of_search_terms = 30


headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

  # Create Folder for every Search Term if not present
def checkFolder(searchString):
    folder_path = '/Users/vineethpenugonda/Documents/Academics/Masters/Semester III/IST 6443/Project/AI_Project/PDFs/' + searchString
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Converting Links To PDFs
def linksToPDF(descriptions, folder_path):
    no_of_downloads = 0
    no_of_ignoredFiles = 0

    for count in range(len(descriptions)):
        try:
            HTML(descriptions[count]).write_pdf(folder_path + "/" + str(count) + '.pdf')
            print("Downloaded: " + descriptions[count] + "\n")
            no_of_downloads = no_of_downloads + 1
        except:
            print("\nIgnoring: " + descriptions[count] + "\n")
            no_of_ignoredFiles = no_of_ignoredFiles + 1
    
    print("\nDownloaded: " + str(no_of_downloads) + "\n")
    print("Ignored: " + str(no_of_ignoredFiles) + "\n")
    print("\n-------------------------------------------------\n")


for searchString in search_term:
    params  = {"q": searchString, "textDecorations": True, "textFormat": "HTML", "count": no_of_search_terms}
    print("\nQuery Term: " + searchString + "\n")
    try:
	    response = requests.get(search_url, headers=headers, params=params)
	    response.raise_for_status()
	    search_results = response.json()
    except:
    	print("\nServer Error!\n")

    # Write URLs to List
    descriptions = [article["url"] for article in search_results["value"]]
    
    # Check if Folder exists or not
    folderPath = checkFolder(searchString)
    
    # Download all Links
    linksToPDF(descriptions, folderPath)

    print("\nSleeping for 5 seconds...\n")
    time.sleep(5)



