"""
Baseline influencer data for comparison.
This would normally be precomputed, but for MVP we hardcode representative values.
"""

BASELINE_INFLUENCERS = {
    'benjamin_cowen': {
        'name': 'Benjamin Cowen',
        'metrics': {
            'emotional_intensity': 25.0,
            'certainty_index': 35.0,
            'technical_depth': 72.0,
            'prediction_density': 42.0,
            'historical_accuracy': 65.0
        }
    },
    'willy_woo': {
        'name': 'Willy Woo',
        'metrics': {
            'emotional_intensity': 45.0,
            'certainty_index': 58.0,
            'technical_depth': 85.0,
            'prediction_density': 55.0,
            'historical_accuracy': 58.0
        }
    },
    'raoul_pal': {
        'name': 'Raoul Pal',
        'metrics': {
            'emotional_intensity': 68.0,
            'certainty_index': 72.0,
            'technical_depth': 65.0,
            'prediction_density': 70.0,
            'historical_accuracy': 52.0
        }
    }
}


def get_baseline_stats():
    """Calculate baseline statistics from reference influencers."""
    all_metrics = [inf['metrics'] for inf in BASELINE_INFLUENCERS.values()]
    
    # Calculate medians
    emotional_values = [m['emotional_intensity'] for m in all_metrics]
    certainty_values = [m['certainty_index'] for m in all_metrics]
    technical_values = [m['technical_depth'] for m in all_metrics]
    accuracy_values = [m['historical_accuracy'] for m in all_metrics]
    
    return {
        'median_emotional_intensity': sorted(emotional_values)[len(emotional_values)//2],
        'median_certainty_index': sorted(certainty_values)[len(certainty_values)//2],
        'median_technical_depth': sorted(technical_values)[len(technical_values)//2],
        'median_historical_accuracy': sorted(accuracy_values)[len(accuracy_values)//2],
        'influencer_count': len(BASELINE_INFLUENCERS)
    }


def compare_to_baseline(user_metrics: dict, user_accuracy: float):
    """
    Compare user metrics to baseline influencers.
    
    Returns comparative metrics like hype_multiplier, accuracy_rank, etc.
    """
    baseline = get_baseline_stats()
    
    # Calculate multipliers and deviations
    hype_multiplier = user_metrics['emotional_intensity'] / max(baseline['median_emotional_intensity'], 1)
    certainty_deviation = user_metrics['certainty_index'] - baseline['median_certainty_index']
    technical_deviation = user_metrics['technical_depth'] - baseline['median_technical_depth']
    
    # Accuracy percentile rank
    accuracy_values = [inf['metrics']['historical_accuracy'] for inf in BASELINE_INFLUENCERS.values()]
    accuracy_values.append(user_accuracy)
    accuracy_values.sort()
    accuracy_rank = (accuracy_values.index(user_accuracy) / len(accuracy_values)) * 100
    
    # Calibration gap comparison
    user_calibration_gap = user_metrics['certainty_index'] - user_accuracy
    baseline_gaps = [
        inf['metrics']['certainty_index'] - inf['metrics']['historical_accuracy']
        for inf in BASELINE_INFLUENCERS.values()
    ]
    baseline_gaps.append(user_calibration_gap)
    baseline_gaps.sort()
    calibration_rank = (baseline_gaps.index(user_calibration_gap) / len(baseline_gaps)) * 100
    
    return {
        'hype_multiplier': round(hype_multiplier, 2),
        'certainty_deviation': round(certainty_deviation, 1),
        'technical_deviation': round(technical_deviation, 1),
        'accuracy_percentile': round(accuracy_rank, 0),
        'calibration_percentile': round(calibration_rank, 0),
        'baseline_stats': baseline
    }