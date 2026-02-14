"""
LLM explanation layer using Claude API.
Generates narrative credibility analysis from structured metrics.
"""

import os
import anthropic
from typing import Dict


def generate_credibility_explanation(
    influencer_name: str,
    metrics: Dict,
    credibility_score: float,
    calibration_gap: float,
    flags: Dict,
    baseline_comparison: Dict,
    evidence: Dict,
    historical_accuracy: float
) -> str:
    """
    Generate AI-powered credibility explanation using Claude.
    
    Args:
        influencer_name: Name of the influencer
        metrics: Raw metric scores
        credibility_score: Composite credibility score
        calibration_gap: Certainty minus accuracy
        flags: Boolean flags (overconfident, high_hype_low_accuracy, etc.)
        baseline_comparison: Comparison to baseline influencers
        evidence: Sample quotes and predictions
        historical_accuracy: Historical prediction accuracy
        
    Returns:
        Structured explanation text
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Build the prompt
    prompt = f"""You are analyzing the credibility of crypto influencer "{influencer_name}".

You have been provided with QUANTIFIED METRICS, not subjective opinions:

**CORE METRICS:**
- Emotional Intensity: {metrics['emotional_intensity']}/100 (higher = more hype language)
- Certainty Index: {metrics['certainty_index']}/100 (higher = more certain language)
- Technical Depth: {metrics['technical_depth']}/100 (higher = more technical)
- Prediction Density: {metrics['prediction_density']}/100 (frequency of predictions)
- Historical Accuracy: {historical_accuracy}/100 (verified prediction success rate)

**CREDIBILITY SCORE: {credibility_score}/100**

**CALIBRATION GAP: {calibration_gap}**
(This is Certainty Index minus Historical Accuracy. Large positive gaps indicate overconfidence.)

**BASELINE COMPARISON:**
- {baseline_comparison['hype_multiplier']}x the emotional intensity of median baseline influencer
- Certainty is {baseline_comparison['certainty_deviation']:+.0f} points vs baseline median
- Historical accuracy is at the {baseline_comparison['accuracy_percentile']:.0f}th percentile
- Calibration gap is at the {baseline_comparison['calibration_percentile']:.0f}th percentile

**ACTIVE FLAGS:**
{_format_flags(flags)}

**SAMPLE EVIDENCE:**
High-certainty quotes: {evidence.get('certainty_quotes', [])[:3]}
High-intensity quotes: {evidence.get('intensity_quotes', [])[:3]}
Technical quotes: {evidence.get('technical_quotes', [])[:3]}

---

Write a credibility analysis that:
1. Explains what the credibility score means (2-3 sentences)
2. Identifies key strengths (if any)
3. Identifies key weaknesses (if any)
4. Contextualizes them vs baseline influencers
5. Focuses on CALIBRATION: does their confidence match their accuracy?

Be analytical, not judgmental. Be concise (under 200 words). No bullet points. Write in clear prose.
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except Exception as e:
        # Fallback explanation if API fails
        return f"Credibility score: {credibility_score}/100. Calibration gap of {calibration_gap} suggests {'overconfidence' if calibration_gap > 20 else 'reasonable calibration'}. Analysis service temporarily unavailable."


def _format_flags(flags: Dict) -> str:
    """Format boolean flags into readable text."""
    active = [name.replace('_', ' ').title() for name, value in flags.items() if value]
    if not active:
        return "None"
    return ", ".join(active)