from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.app_logic import analyze_channel

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    channel_id = data.get("channel_id")
    influencer_name = data.get("influencer_name", "Unknown")
    max_videos = data.get("max_videos", 3)

    if not channel_id:
        return jsonify({"error": "channel_id is required"}), 400

    result = analyze_channel(channel_id, influencer_name, max_videos)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
