
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 10:57:03 2021

@author: Maleknaz
Edited by: Elim Lemango
"""
import scrapy
import sys
import os
import json
from bs4 import BeautifulSoup
import requests# Request to website and download HTML contents
import time

from cherrypicker import CherryPicker
import json
import pandas as pd
import csv

#Note THIS PYTHON SCRIPT DOES MAKE REQUESTS TO THE SO API BUT IT DOESNT REALLY MAKE THE JSON FILES
# IT ONLY MAKES THE CSV FILES

exceptions = open("exceptionlist.txt", "w" )

APIs = open("one_API.csv", "r")
#headers = {'Key': ''}


for row in APIs:
    APInames = APIs.readline()
    APIname = APInames.splitlines()
    print("*******" + APInames)
    all_items = []
    myCSV = pd.DataFrame() # this is a completely empty Dataframe without any column names, indices or data
    page_count = 1 #  counter for the API request
    json_count = 0 #  counter for the json files
    try:
        # API request using stackexchange API
        query = "https://api.stackexchange.com/2.3/search/advanced?key=BmopG%29d9Thccirg4e%29CjOw%28%28&page="+ str(page_count)+ "&pagesize=100&order=desc&sort=activity&q=" +  row + "&site=stackoverflow"
        print("***** Page Count =" + str(page_count))
        req=requests.get(query)
        Fj=req.json()
        myJ = json.loads(req.text)
        #myJdata = json.dumps(myJ)

        #flatten the file
        picker = CherryPicker(myJ)
        #print(myJdata['has_more'])
        flat = picker['items'].flatten().get()
        df = pd.DataFrame(flat)

        myCSV = df[['owner_user_id','owner_account_id','question_id','owner_reputation']]
        myCSV['API_Name'] = str(row.strip())
        myCSV.to_csv(row.strip() + "_All_Pages_T" + ".csv")

        all_items.append(Fj)  #append the items on to list all items[] (the ones on the first page)
        num_pages = myJ['has_more']
        print(myJ['has_more'])
        while (num_pages == True):
            page_count = page_count + 1
            query = "https://api.stackexchange.com/2.3/search/advanced?key=BmopG%29d9Thccirg4e%29CjOw%28%28&page="+ str(page_count) + "&pagesize=100&order=desc&sort=activity&q=" +  row + "&site=stackoverflow"
            print("***** Page Count =" + str(page_count))
            req=requests.get(query)
            j=req.json()
            dicJ = json.loads(req.text)
            
             #flatten the file
            picker = CherryPicker(dicJ)
            flat = picker['items'].flatten().get()
            df = pd.DataFrame(flat)

            myCSV = df[['owner_user_id','owner_account_id','question_id','owner_reputation']]
            myCSV['API_Name'] = str(row.strip())
            myCSV.to_csv(row.strip() + "_All_Pages_T" + ".csv",  header=None, mode='a')

            num_pages = dicJ['has_more']
            print(dicJ['has_more'])
            all_items.append(j)  #append the items onto list all items[]
        # After you see that it has no more pages   
        print("No more Pages")
        #resultFile = open(row.strip() + "_All_Pages" + ".json", "w")
        #json.dump(all_items, resultFile)
       # resultFile.close()
    except IndexError:
            exceptions.write(APInames + "\n")
      
print("C'est fini!!!!!!!")