from flask import Flask, request, jsonify
import requests
from requests_oauthlib import OAuth1
import os

app = Flask(__name__)

# Get Tumblr API credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
OAUTH_SECRET = os.getenv("OAUTH_SECRET")
BLOG_NAME = os.getenv("BLOG_NAME")

@app.route("/")
def home():
    return "Fiction Feast Submission API is Running!"

@app.route("/submit", methods=["POST"])
def submit_book():
    print("🔹 Received a request at /submit")  # Debugging step
    
    # Check if JSON data is received
    if not request.is_json:
        print("❌ Error: No JSON received")  # Debugging step
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json

    print(f"📖 Received book data: {data}")  # Debugging step

    title = data.get("title")
    author = data.get("author")
    summary = data.get("summary")
    tags = data.get("tags", "")

    if not title or not author or not summary:
        print("❌ Error: Missing required fields")  # Debugging step
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify({"message": "Submission received!"})


    # Format Tumblr post
    post_data = {
        "type": "text",
        "title": f"{title} by {author}",
        "body": summary,
        "tags": tags,
    }

    # Authenticate with Tumblr API
    oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    tumblr_url = f"https://api.tumblr.com/v2/blog/{BLOG_NAME}/post"

    response = requests.post(tumblr_url, auth=oauth, data=post_data)

    if response.status_code == 201:
        return jsonify({"message": "Submission successful", "tumblr_response": response.json()})
    else:
        return jsonify({"error": "Tumblr submission failed", "details": response.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/routes", methods=["GET"])
def show_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])
