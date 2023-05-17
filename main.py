import requests
import selectorlib
import time
import streamlit as sl
import plotly.express as px
from datetime import datetime

url = 'http://programmer100.pythonanywhere.com/'

def scrape(url):
    #scrape data from website
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("data.yaml")
    avgtemp = extractor.extract(source)['avgtemp']
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(timestamp, avgtemp)
    return (timestamp, avgtemp)

def slchart(dates, values, chope):
    figure = px.line(x=dates, y=values,
                     labels={'x': 'Date', 'y': 'Temperature (C)'})
    with chope:
        sl.plotly_chart(figure)


if __name__ =="__main__":
    sl.header('average world temperatures')
    #'reserves' an empty space for a static item that updates with dynamic data
    chope = sl.empty()
    templist = []
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        templist.append(extracted)
        time.sleep(2)

        #print(templist)
        #print(zip(*templist))

        xy = list(zip(*templist))
        #print(xy)
        dates = tuple(xy[0])
        values = tuple(xy[1])
        slchart(dates, values, chope)


