#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


from bs4 import BeautifulSoup
import requests
import cloudscraper
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import random

print("Welcome! Note that this program requires FireFox Browser to run successfully")
input("\nPress Enter to begin scraping: ")
loading = "\nSuccesfully Loaded Software, Scraping Initiating"
for letter in list(loading):
    time.sleep(random.uniform(0,0.2))
    print(letter, end='', flush=True)
print(".", end='', flush=True)
time.sleep(0.5)
print(".", end='', flush=True)
time.sleep(0.5)
print(".", end='', flush=True)
time.sleep(0.5)
print(".", end='', flush=True)
time.sleep(0.5)
print(".", end='', flush=True)
time.sleep(0.5)

# Initialize the Chrome driver
driver = webdriver.Firefox()
# Open the webpage
driver.get("https://www.globalair.com/aircraft-for-sale/private-jet")

# Continuously click the 'Load More' button until all items are loaded

cookie = driver.find_element(By.XPATH, '//*[@id="cookie-notification-btn-N"]')
cookie.click()

while True:
    try:
        time.sleep(0.5)
        load_more_button = driver.find_element(By.XPATH, '//*[@id="loadPageX"]')  # Use the correct ID or XPath for the button
        load_more_button.click()
            # Wait for the data to load
    except:
        break

page_source = driver.page_source

driver.quit()

time.sleep(1)
print("\n\nData Scraped Succesfully. Now Formatting Results.\n")

soup = BeautifulSoup(page_source, "lxml")


# In[2]:


box = soup.find_all('div', class_='listing-price')
modelYear = soup.find_all('a', class_='result-title')
rightColumn = soup.find_all('div', class_='col pb-2 right-info')
noListedYear = 0
callCount = 0
dollarCount = 0
modelYearList = []
priceList = []
priceListint = []
recordPrice = []
info = []
RN = []
RN2 = []
SN = []
SN2 = []
TT = []
TT2=[]
cumTT = []
masterList = []

for n in box:
    price = n.text.split(":")
    price2 = price[-1].split(" ")
    priceList.append(price2[-1])
for p in priceList:
    try:
        dollar = p.split("$")
        dollarReal = dollar[-1].replace(",", "")
        priceListint.append(int(dollarReal))
        recordPrice.append(int(dollarReal))
        dollarCount+=1
    except:
        callCount+=1
        recordPrice.append("No price")
        pass
for n in modelYear:
    year = n.text.split(" ")
    removeSpace = year[0].replace("\n","")
    try:
        modelYearList.append(int(removeSpace))
    except:
        modelYearList.append("No Year")
        noListedYear+=1
        pass

for n in rightColumn:
    sepVar = n.text.split("\n")
    info.append(sepVar)
for k in info:
    TT.append(k[2])
    SN.append(k[3])
    RN.append(k[4])
for x in TT:
    sep1 = x.split(": ")
    remstr = sep1[-1].replace(" hrs", "")
    remstr1 = remstr.replace(",","")
    try:
        TT2.append(int(remstr1))
        cumTT.append(int(remstr1))
    except:
        TT2.append("No TT")
        pass
for y in SN:
    sepSN = y.split(": ")
    if sepSN[-1] == '':
        SN2.append('No SN')
    else:
        SN2.append(sepSN[-1])
for z in RN:
    sepRN = z.split(": ")
    if sepRN[-1] == '':
        RN2.append('No RN')
    else:
        RN2.append(sepRN[-1])
for a,b,c,d,e in zip(modelYearList,recordPrice,TT2,SN2,RN2):
    transientList = []
    transientList.append(a)
    transientList.append(b)
    transientList.append(c)
    transientList.append(d)
    transientList.append(e)
    masterList.append(transientList)

cumulativeAveragePrice = str(round((sum(priceListint)/len(priceListint)), 2))
cumulativeAverageTT = str(round((sum(cumTT)/len(cumTT)), 2))


# In[3]:


from collections import defaultdict
from datetime import date
yearly_data = defaultdict(list)
stryearly_data = defaultdict(list)
SN_data = defaultdict(list)
strSN_data = defaultdict(list)
RN_data = defaultdict(list)
strRN_data = defaultdict(list)

today = date.today()

for record in masterList:
    year, price, travel_time,serial_number,record_number = record
    if isinstance(year, int) and year is not None:
        yearly_data[year].append((price, travel_time))
        SN_data[year].append(serial_number)
        RN_data[year].append(record_number)
    else:
        stryearly_data[year].append((price, travel_time))
        strSN_data[year].append(serial_number)
        strRN_data[year].append(record_number)
        
averages_by_year = {}
straverages_by_noyear = {}
def averager(averages_by_year, yearly_data):

    for year, values in yearly_data.items():
        noPriceCount = 0
        noTTCount = 0
        countPrice = 0
        countTT = 0
        total_price = sum(price for price, _ in values if isinstance(price, (int, float)))

        for price, _ in values:
            if isinstance(price, (int, float)):
                countPrice+=1
            else:
                noPriceCount += 1
        total_travel_time = sum(travel_time for _, travel_time in values if isinstance(travel_time, (int, float)))
        for _, travel_time in values:
            if isinstance(travel_time, (int, float)):
                countTT+=1
            else:
                noTTCount += 1
        try:
            avg_price = total_price / countPrice
        except:
            avg_price = "No samples to average"
        try:
            avg_travel_time = total_travel_time / countTT
        except:
            avg_travel_time = "No samples to average"
        try:
            averages_by_year[year] = (round(avg_price,2), round(avg_travel_time,2),countPrice, countTT, noPriceCount, noTTCount, (countPrice+noPriceCount), (countTT + noTTCount))
        except:
            averages_by_year[year] = (avg_price, avg_travel_time, countPrice, countTT, noPriceCount, noTTCount, (countPrice+noPriceCount), (countTT + noTTCount))
    return averages_by_year

avgyear = averager(averages_by_year, yearly_data)
stryearlyavg = averager(straverages_by_noyear, stryearly_data)

sorted_keys = sorted(avgyear.keys())
sorted_pricecums = []
sorted_TTcums = []
sorted_price = []
sorted_TT = []
sorted_noprice = []
sorted_noTT = []
sorted_pricetotal = []
sorted_TTTotal = []
dateFiller = [today]
cum_avg_price_filler = [cumulativeAveragePrice]
cum_avg_TT_filler = [cumulativeAverageTT]
aircraftsFound = [len(masterList)]
spacer = []

for item in sorted_keys:
    sorted_pricecums.append(avgyear[item][0])
    sorted_TTcums.append(avgyear[item][1])
    sorted_price.append(avgyear[item][2])
    sorted_TT.append(avgyear[item][3])
    sorted_noprice.append(avgyear[item][4])
    sorted_noTT.append(avgyear[item][5])
    sorted_pricetotal.append(avgyear[item][6])
    sorted_TTTotal.append(avgyear[item][7])

sorted_keys.append("No Year")
sorted_pricecums.append(stryearlyavg["No Year"][0])
sorted_TTcums.append(stryearlyavg["No Year"][1])
sorted_price.append(stryearlyavg["No Year"][2])
sorted_TT.append(stryearlyavg["No Year"][3])
sorted_noprice.append(stryearlyavg["No Year"][4])
sorted_noTT.append(stryearlyavg["No Year"][5])
sorted_pricetotal.append(stryearlyavg["No Year"][6])
sorted_TTTotal.append(stryearlyavg["No Year"][7])

def listExtender(inputList, parentList):
    inputList.extend(['']*(len(parentList)-len(inputList)))
    return inputList

listExtender(sorted_keys, masterList)
listExtender(sorted_pricecums, masterList)
listExtender(sorted_TTcums, masterList)
listExtender(sorted_price, masterList)
listExtender(sorted_TT, masterList)
listExtender(sorted_noprice, masterList)
listExtender(sorted_noTT, masterList)
listExtender(sorted_pricetotal, masterList)
listExtender(sorted_TTTotal, masterList)
listExtender(dateFiller, masterList)
listExtender(cum_avg_price_filler, masterList)
listExtender(cum_avg_TT_filler, masterList)
listExtender(aircraftsFound, masterList)
listExtender(spacer, masterList)


# In[ ]:


import csv
import pandas as pd

rowA = {'Data Collection Date': dateFiller, "Total Aircrafts Found": aircraftsFound, "Cumulative Average Price (USD)": cum_avg_price_filler, "Cumulative Average TT (hrs)": cum_avg_TT_filler, "Year": sorted_keys, "Total Aircrafts With Listed Price By Year": sorted_price, "Total Aircrafts with Listed TT By Year": sorted_TT, "Total Aircrafts By Year": sorted_pricetotal, "Average Price By Year (USD)": sorted_pricecums, "Average TT By Year (hrs)": sorted_TTcums}

df = pd.DataFrame(rowA)
dfSN = pd.DataFrame()
dfRN = pd.DataFrame()

def fml(dictionary):
    base_list = []
    for length in dictionary:
        base_list.append(dictionary[length])
    list_len = [len(i) for i in base_list]
    return max(list_len)

SN_data = sorted_SN_data = {key: SN_data[key] for key in sorted(SN_data.keys())}
RN_data = sorted_SN_data = {key: RN_data[key] for key in sorted(RN_data.keys())}

if fml(SN_data) > fml(strSN_data):
    SN_max = fml(SN_data)
else:
    SN_max = fml(strSN_data)
if fml(RN_data) > fml(strRN_data):
    RN_max = fml(RN_data)
else:
    RN_max = fml(strRN_data)

def add_to_SNRN(dict1, dict2):
    for S1,R1 in zip(dict1,dict2):
        dict1[S1].extend(['']* (SN_max - len(dict1[S1])))
        dfSN[S1] = dict1[S1]
        dict2[R1].extend(['']* (RN_max - len(dict2[R1])))
        dfRN[R1] = dict2[R1]

add_to_SNRN(SN_data,RN_data)
add_to_SNRN(strSN_data,strRN_data)

fileName = "aircraft_data_" + str(today) + ".csv"
SN_file = "SN_data_" + str(today) + ".csv"
RN_file = "RN_data_" + str(today) + ".csv"

try:
    with open(fileName, mode='w', newline='') as file:
        writer = csv.writer(file)
    with open(SN_file, mode='w', newline='') as file:
        writer = csv.writer(file)
    with open(RN_file, mode='w', newline='') as file:
        writer = csv.writer(file)

    df.to_csv(fileName, index=False)
    dfSN.to_csv(SN_file, index=False)
    dfRN.to_csv(RN_file, index=False)
except:
    print("an error has occured, ensure that you have closed excel and try again.")

print("\n\nFile Created and Data Exported Succesfully!!")
print("\nFile name = " + fileName + " (exported to the same file location as this program)")
print("\nFile name = " + SN_file + " (exported to the same file location as this program)")
print("\nFile name = " + RN_file + " (exported to the same file location as this program)")

input("Press any key to exit the program")
print("\n\nClosing Application")
exit()
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




