from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return full_text

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."

    except NoTranscriptFound:
        return "No transcript found."

    except Exception as e:
        return f"ERROR: {str(e)}"
