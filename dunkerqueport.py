# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 12:06:12 2021

@author: SaimonBombi
"""
import sys
import subprocess
import os
from datetime import datetime

# check if scrapy package is installed, if not pip install
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'scrapy'])

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

# check if pandas package is installed, if not pip install
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'pandas'])

import pandas as pd

#Scrapy Crawler script: goes to bordeaux-port web and scrolls the data requested of the ships

class dunkerqueportSpider(scrapy.Spider):
    name = 'dunkerqueport'
    start_urls = ['http://www.dunkerque-port.fr/fr/activites-commerciales/navires-entree-transit.html']
    custom_settings = {"FEEDS": {"dunkerqueport.csv": {"format": "csv"}}}


    def parse(self, response):
        for items in response.css("div.modules-dunkerque-shipflow.modules-dunkerque"):
            for row in items.css("tr.row-0"):
                yield {
                    "name" : row.css("td:nth-child(2)::text").get(),
                    "date" : row.css("td:nth-child(1)::text").get(),
                    "post" : row.css("td:nth-child(6)::text").get(),
                    "origin" : row.css("td:nth-child(5)::text").get(),
                    "destination" : row.css("td:nth-child(7)::text").get()
                    }


# run scrapy crawler inside the Twisted reactor
process = CrawlerProcess(settings={"FEEDS": {"dunkerqueport.csv": {"format": "csv"}}})

process.crawl(dunkerqueportSpider)
process.start() 

#Finished Scrapy crawler
# Created bordeauxport.csv with the last data available. Used CSV to be more easily readable with pandas
# Load cvs into a variable and formatting table

newdata = pd.read_csv("dunkerqueport.csv")
newdata = newdata.dropna(subset=["date", "name"])
newdata["name"] = newdata["name"].fillna(value="Empty Field")

#Load previous data saved as "bordeauxporthistoric.csv"
try:
    dunkerqueporthistoric = pd.read_csv("dunkerqueporthistoric.csv")
except:
    print("dunkerqueporthistoric.csv coudn't be found, continuing with fresh start")
    dunkerqueporthistoric = pd.DataFrame(columns=['name', 'post', 'date', 'origin', "destination"])

newdatadict = newdata.to_dict()

#print date time
nowdatetime = datetime.now()
nowdatetime = nowdatetime.strftime("%d/%m/%Y %H:%M:%S")
print("Date and time = " + nowdatetime,  file=open('dunkerqueportreport.txt', 'a'))

#Loop that checks if a new ship is appeared and adds it to the historic file. 
#If is already there, check for the date. Print report while working

for i in newdatadict["name"]:
    #print(newdatadict["name"][i])
    x = dunkerqueporthistoric.loc[dunkerqueporthistoric['name'] == (newdatadict["name"][i])]
    if x.empty == True:
        print("NEW SHIP! name: " + newdatadict["name"][i],  file=open('dunkerqueportreport.txt', 'a'))
        dunkerqueporthistoric = dunkerqueporthistoric.append({
            "name": newdatadict["name"][i],
            "date": newdatadict["date"][i],
            "post": newdatadict["post"][i],
            "comingfrom": newdatadict["origin"][i],
            "destination": newdatadict["destination"][i]},
             ignore_index=True
        )
        print("Ship added",  file=open('dunkerqueportreport.txt', 'a'))
    if x.empty == False:
        print("Ship name: " + newdatadict["name"][i] + " already here",  file=open('dunkerqueportreport.txt', 'a'))
        samedate = x["date"][x.index] == newdatadict["date"][i]
        if samedate.item() == True:
            print("Same ETA as before, no updates needed",  file=open('dunkerqueportreport.txt', 'a'))
        if samedate.item() == False:
            print("Has been a change in ETA in this ship",  file=open('dunkerqueportreport.txt', 'a'))
            dunkerqueporthistoric = dunkerqueporthistoric.drop(index=x.index)
            dunkerqueporthistoric = dunkerqueporthistoric.append({
            "name": newdatadict["name"][i],
            "date": newdatadict["date"][i],
            "post": newdatadict["post"][i],
            "comingfrom": newdatadict["origin"][i],
            "destination": newdatadict["destination"][i]},
             ignore_index=True)
            print("Ship updated",  file=open('dunkerqueportreport.txt', 'a'))

#save table in bordeauxporthistoric.csv
to_save = dunkerqueporthistoric

print("Table updated. This is the updated table",  file=open('dunkerqueportreport.txt', 'a'))
print(dunkerqueporthistoric, file=open('dunkerqueportreport.txt', 'a'))
print("Saving table in bordeauxporthistoric.csv",  file=open('dunkerqueportreport.txt', 'a'))

try:
    to_save.to_csv("dunkerqueporthistoric.csv", index=False)
except:
    print("Coudn't save dunkerqueporthistoric.csv",  file=open('dunkerqueportreport.txt', 'a'))

#Delete bordeauxport.csv because the next time the script will run it's going to write new data in the end of the file and keeps stacking duplicate data

try:    
    os.remove("dunkerqueport.csv")
except:
    print("Coudn't delete dunkerqueport.csv , check manually before running script again",  file=open('dunkerqueportreport.txt', 'a'))




