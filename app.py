from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from services.youtube import get_recent_videos, enrich_videos
from services.transcript import get_transcript

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    channel_id = request.form["channel_id"]

    # Step 1: Get recent videos (basic info)
    videos = get_recent_videos(channel_id, max_results=5)

    if not videos:
        return "No videos found for this channel."

    # Step 2: Extract video IDs
    video_ids = [video["video_id"] for video in videos]

    # Step 3: Enrich with metadata (views, likes, etc.)
    enriched_videos = enrich_videos(video_ids)

    # Step 4: Add transcript to each video
    for video in enriched_videos:
        transcript = get_transcript(video_ids[enriched_videos.index(video)])
        video["transcript"] = transcript[:1000]  # truncate so page doesn’t explode

    # Step 5: Display output
    output = "<h2>Video Analysis</h2><ul>"

    for video in enriched_videos:
        output += f"""
        <li>
        <strong>{video['title']}</strong><br>
        Views: {video['views']}<br>
        Likes: {video['likes']}<br>
        Published: {video['published_at']}<br>
        Transcript Preview:<br>
        {video['transcript']}<br><br>
        </li>
        """

    output += "</ul>"

    return output


if __name__ == "__main__":
    app.run(debug=True)
