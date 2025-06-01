from typing import Optional
import pymongo
from pymongo import MongoClient

import chainlit as cl


def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        return client
    except pymongo.errors.ConnectionFailure:
        raise Exception("Failed to connect to MongoDB.")

# @cl.password_auth_callback
def password_auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    try:
        client = connect_to_mongo()
        db = client["user_database"]
        collection = db["username_and_password"]

        user = collection.find_one({"username": username})
        if user and user["password"] == password:
            print("User authenticated successfully")
            return cl.User(
                identifier=username,
                metadata={"role": "user", "provider": "credentials"},
            )
        return None
    
    except Exception as e:
        raise Exception(f"Failed to sign in: {str(e)}")