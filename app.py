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

@app.route("/submit", methods=["GET", "POST"])
def submit_book():
    print(f"🛑 Incoming request method: {request.method}")  # Debugging request type
    
    if request.method == "GET":
        return jsonify({"error": "Use POST method to submit books"}), 405

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

    print("📡 Sending request to Tumblr API...")
    response = requests.post(tumblr_url, auth=oauth, data=post_data)

    if response.status_code == 201:
        print("✅ Tumblr submission successful!")  # Debugging success
        return jsonify({"message": "Submission successful", "tumblr_response": response.json()})
    else:
        print(f"❌ Tumblr submission failed: {response.text}")  # Debugging failure
        return jsonify({"error": "Tumblr submission failed", "details": response.text}), 500

@app.route("/routes", methods=["GET"])
def show_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

# Ensure Flask runs on the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from Render
    app.run(host="0.0.0.0", port=port)
