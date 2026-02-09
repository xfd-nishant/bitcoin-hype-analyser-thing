from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from services.youtube import get_recent_videos

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    channel_id = request.form["channel_id"]

    videos = get_recent_videos(channel_id, max_results=5)

    output = "<h2>Recent Videos:</h2><ul>"
    for video in videos:
        output += f"<li>{video['title']}</li>"
    output += "</ul>"

    return output

if __name__ == "__main__":
    app.run(debug=True)
