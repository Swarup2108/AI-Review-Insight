from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["SentimentDB"]

collection = db["Reviews"]