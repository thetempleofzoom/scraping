import requests
import selectorlib
import time
import streamlit as sl
import plotly.express as px
from datetime import datetime
import sqlite3

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

def store(extracted):
    cursor.execute("INSERT INTO temperature VALUES(?,?)", extracted)
    connection.commit()

def slchart(dates, values, chope):
    figure = px.line(x=dates, y=values,
                     labels={'x': 'Date', 'y': 'Temperature (C)'})
    with chope:
        sl.plotly_chart(figure)


if __name__ =="__main__":
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    #delete previous table values
    cursor.execute("DELETE FROM temperature")
    connection.commit()
    
    sl.header('average world temperatures')
    #'reserves' an empty space for a static item that updates with dynamic data
    chope = sl.empty()
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        store(extracted)
        time.sleep(2)

        cursor.execute("SELECT * FROM temperature")
        rows = cursor.fetchall()
        #print(rows)

        testrows = list(zip(*rows))
        #print(tuple(testrows))
        dates = testrows[0]
        values = testrows[1]
        #print(dates)
        #print(values)
        slchart(dates, values, chope)


