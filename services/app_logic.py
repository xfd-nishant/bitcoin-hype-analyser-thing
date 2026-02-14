from services.audio import download_audio
from services.transcribe import transcribe_audio
from services.metrics import MetricsExtractor, calculate_credibility_score
from services.baseline import compare_to_baseline
from services.llm_analysis import generate_credibility_explanation
from services.storage import save_analysis_result, get_historical_accuracy
import json


def get_video_list(video_urls):
    """Convert list of URLs into dict format expected by pipeline."""
    videos = []
    for url in video_urls:
        video_id = url.split("v=")[-1]
        videos.append({
            "video_id": video_id,
            "title": f"Video {video_id[:6]}"  # placeholder title
        })
    return videos


def analyze_channel(channel_id: str, influencer_name: str = None, max_videos: int = 3):
    """
    Complete analysis pipeline for a YouTube channel.
    Uses local MVP video URLs for testing.
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING CHANNEL: {channel_id}")
    print(f"{'='*60}\n")

    # MVP video URLs
    video_urls = [
        "https://www.youtube.com/watch?v=abc123",
        "https://www.youtube.com/watch?v=def456",
        "https://www.youtube.com/watch?v=ghi789"
    ]
    videos = get_video_list(video_urls)
    print(f"  {len(videos)} videos selected for analysis\n")

    all_transcripts = []
    video_metadata = []

    for i, video in enumerate(videos, 1):
        video_url = f"https://www.youtube.com/watch?v={video['video_id']}"
        print(f"  [{i}/{len(videos)}] {video['title']}...")
        try:
            audio_path = download_audio(video_url)
            transcript = transcribe_audio(audio_path)
            all_transcripts.append(transcript)
            video_metadata.append({
                'title': video['title'],
                'video_id': video['video_id'],
                'word_count': len(transcript.split())
            })
            print(f"      ✓ Transcribed ({len(transcript.split())} words)")
        except Exception as e:
            print(f"      ✗ Failed: {e}")

    combined_transcript = " ".join(all_transcripts)
    total_words = len(combined_transcript.split())
    print(f"\n→ Total content: {total_words:,} words\n")

    # Extract metrics
    extractor = MetricsExtractor()
    extraction_result = extractor.extract_all_metrics(combined_transcript)
    metrics = extraction_result['metrics']
    predictions = extraction_result['predictions']
    evidence = extraction_result['evidence']

    # Historical accuracy
    historical_accuracy = get_historical_accuracy(channel_id)

    # Credibility score
    credibility_result = calculate_credibility_score(metrics, historical_accuracy)
    credibility_score = credibility_result['credibility_score']
    calibration_gap = credibility_result['calibration_gap']
    flags = credibility_result['flags']

    # Baseline comparison
    baseline_comparison = compare_to_baseline(metrics, historical_accuracy)

    # AI explanation
    ai_explanation = generate_credibility_explanation(
        influencer_name=influencer_name or "This Influencer",
        metrics=metrics,
        credibility_score=credibility_score,
        calibration_gap=calibration_gap,
        flags=flags,
        baseline_comparison=baseline_comparison,
        evidence=evidence,
        historical_accuracy=historical_accuracy
    )

    # Assemble final result
    final_result = {
        'influencer_name': influencer_name or "Unknown",
        'channel_id': channel_id,
        'analysis_summary': {
            'videos_analyzed': len(all_transcripts),
            'total_words': total_words
        },
        'metrics': metrics,
        'credibility_score': credibility_score,
        'calibration_gap': calibration_gap,
        'historical_accuracy': historical_accuracy,
        'flags': flags,
        'baseline_comparison': baseline_comparison,
        'predictions': predictions[:10],
        'evidence': evidence,
        'ai_explanation': ai_explanation,
        'video_metadata': video_metadata
    }

    save_analysis_result(channel_id, final_result)
    return final_result
