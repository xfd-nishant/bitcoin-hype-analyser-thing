from flask import Flask, request, jsonify, render_template
from services.app_logic import analyze_channel

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Serve HTML from Flask

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    channel_id = data.get("channel_id")
    influencer_name = data.get("influencer_name", None)
    
    if not channel_id:
        return jsonify({"error": "Missing channel_id"}), 400
    
    try:
        result = analyze_channel(channel_id, influencer_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
