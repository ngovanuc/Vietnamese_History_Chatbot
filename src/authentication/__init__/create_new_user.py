import pymongo
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

username = input("Enter username: ")
password = input("Enter password: ")

# Create a new user in the "username_and_password" collection
try:
    db = client["user_database"]
    collection = db["username_and_password"]
    collection.insert_one({"username": username, "password": password})
    print("User created successfully.")
except pymongo.errors.DuplicateKeyError:
    print("User already exists.")