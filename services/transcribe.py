from faster_whisper import WhisperModel

_model = None


def get_model():
    global _model
    if _model is None:
        _model = WhisperModel("base", device="auto", compute_type="auto")
    return _model


def transcribe_audio(audio_path: str) -> str:
    model = get_model()
    segments, _ = model.transcribe(audio_path)

    transcript = ""
    for segment in segments:
        transcript += segment.text + " "

    return transcript.strip()
