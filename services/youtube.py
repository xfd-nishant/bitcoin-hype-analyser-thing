from googleapiclient.discovery import build
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

print("API KEY LOADED:", YOUTUBE_API_KEY is not None)

def get_recent_videos(channel_id, max_results=5):
    youtube = build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY
    )

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    )

    response = request.execute()
    return response["items"]
