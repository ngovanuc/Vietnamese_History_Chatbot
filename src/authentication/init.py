"""Tạo database "user_database" và các "collection" ban đầu để có thể thử nghiệm."""
import pymongo
from pymongo import MongoClient


# Create a connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
if client:
    print("Connected to MongoDB successfully.")
else:
    raise Exception("Failed to connect to MongoDB.")


# Create "user_database"
user_database = "user_database"
if user_database in client.list_database_names():
    print(f"Database {user_database} already exists.")
    # database = client.user_database
else:
    database = client.user_database
    print(f"Database {user_database} created.")


# Create "username_and_password" collection
username_and_password = "username_and_password"
if username_and_password in database.list_collection_names():
    print(f"Collection {username_and_password} already exists.")
    # collection = database.username_and_password
else:
    collection = database.username_and_password
    print(f"Collection {username_and_password} created.")


# Add "admin" username and "admin" password
admin = "admin"
password = "admin"
# Check if username "admin" has already existed
if collection.find_one({"username": admin}):
    print(f"Username {admin} already exists.")
else:
    collection.insert_one({"username": admin, "password": password})
    print(f"Username {admin} created.")


print("Initialization completed.")