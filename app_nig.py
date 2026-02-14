from services.audio import download_audio
from services.transcribe import transcribe_audio
from services.metrics import MetricsExtractor, calculate_credibility_score
from services.baseline import compare_to_baseline
from services.llm_analysis import generate_credibility_explanation
from services.storage import (
    save_analysis_result,
    get_historical_accuracy,
    save_historical_accuracy
)
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


def analyze_channel(channel_id: str, influencer_name: str = None, max_videos: int = 5):
    """
    Complete analysis pipeline for a YouTube channel.
    Uses local MVP list of video URLs instead of live API.
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING CHANNEL: {channel_id}")
    print(f"{'='*60}\n")

    # Step 1: Define MVP videos (hardcoded URLs for now)
    print("→ Using MVP video URLs...")
    video_urls = [
        "https://www.youtube.com/watch?v=abc123",
        "https://www.youtube.com/watch?v=def456",
        "https://www.youtube.com/watch?v=ghi789"
    ]
    videos = get_video_list(video_urls)
    print(f"  {len(videos)} videos selected for analysis\n")

    # Step 2: Download, transcribe, and aggregate
    print("→ Processing videos (download + transcribe)...")
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
    print(f"\n→ Total content: {total_words:,} words from {len(all_transcripts)} videos\n")

    # Step 3: Extract metrics
    print("→ Extracting credibility metrics...")
    extractor = MetricsExtractor()
    extraction_result = extractor.extract_all_metrics(combined_transcript)
    metrics = extraction_result['metrics']
    predictions = extraction_result['predictions']
    evidence = extraction_result['evidence']

    print(f"  Emotional Intensity: {metrics['emotional_intensity']}/100")
    print(f"  Certainty Index: {metrics['certainty_index']}/100")
    print(f"  Technical Depth: {metrics['technical_depth']}/100")
    print(f"  Prediction Density: {metrics['prediction_density']}/100")
    print(f"  Extracted {len(predictions)} predictions\n")

    # Step 4: Historical accuracy
    historical_accuracy = get_historical_accuracy(channel_id)
    print(f"→ Historical Accuracy: {historical_accuracy}/100\n")

    # Step 5: Calculate credibility score
    print("→ Calculating credibility score...")
    credibility_result = calculate_credibility_score(metrics, historical_accuracy)
    credibility_score = credibility_result['credibility_score']
    calibration_gap = credibility_result['calibration_gap']
    flags = credibility_result['flags']

    print(f"  Credibility Score: {credibility_score}/100")
    print(f"  Calibration Gap: {calibration_gap:+.1f}")
    active_flags = [k for k, v in flags.items() if v]
    if active_flags:
        print(f"  Active Flags: {', '.join(active_flags)}")
    print()

    # Step 6: Baseline comparison
    print("→ Comparing to baseline influencers...")
    baseline_comparison = compare_to_baseline(metrics, historical_accuracy)
    print(f"  Hype Multiplier: {baseline_comparison['hype_multiplier']}x")
    print(f"  Certainty Deviation: {baseline_comparison['certainty_deviation']:+.0f} points")
    print(f"  Accuracy Percentile: {baseline_comparison['accuracy_percentile']:.0f}th\n")

    # Step 7: Generate AI explanation
    print("→ Generating AI credibility analysis...")
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

    print(f"\n{'='*60}")
    print("AI CREDIBILITY ANALYSIS")
    print(f"{'='*60}")
    print(ai_explanation)
    print(f"{'='*60}\n")

    # Step 8: Assemble final result
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

    # Step 9: Save result
    save_analysis_result(channel_id, final_result)
    print("→ Analysis saved to storage\n")

    return final_result
'''
if __name__ == "__main__":
    channel_id = input("Enter YouTube channel ID to analyze: ").strip()
    influencer_name = input("Enter influencer name (optional): ").strip() or None

    result = analyze_channel(
        channel_id=channel_id,
        influencer_name=influencer_name,
        max_videos=3
    )
'''