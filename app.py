from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# 🔥 Replace with YOUR connection string
client = MongoClient("mongodb+srv://60304645:<12class34>@web2.0wcr6lw.mongodb.net/?appName=web2")

db = client["event_db"]
collection = db["events"]

@app.route("/")
def home():
    return "App is running"

@app.route("/test-db")
def test_db():
    collection.insert_one({"msg": "connected"})
    return "MongoDB connected successfully!"

if __name__ == "__main__":
    app.run(debug=True)