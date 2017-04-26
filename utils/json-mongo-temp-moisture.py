from pymongo import MongoClient
from datetime import datetime
import urllib, json


client = MongoClient('192.168.188.232:27017')
db = client['dashy']
col = db.get_collection('data-temp-moist')

response = urllib.urlopen("http://192.168.188.160/json")
data = json.loads(response.read())

post = {
    "humidity" : data[0]['humidity'],
    "temperatureC" : data[0]['temperatureC'],
    "temperatureF" : data[0]['temperatureF'],
    "heatIndexF" : data[0]['heatIndexF'],
    "heatIndexC" : data[0]['heatIndexC'],
    "timestamp" : datetime.now()
}

col.insert_one(post)