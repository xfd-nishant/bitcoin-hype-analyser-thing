"""
Simple JSON storage for analysis results.
In production, this would be a proper database.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


STORAGE_DIR = "/home/claude/data"
RESULTS_FILE = os.path.join(STORAGE_DIR, "analysis_results.json")
ACCURACY_FILE = os.path.join(STORAGE_DIR, "historical_accuracy.json")


def ensure_storage():
    """Ensure storage directory exists."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(ACCURACY_FILE):
        with open(ACCURACY_FILE, 'w') as f:
            json.dump({}, f)


def save_analysis_result(channel_id: str, result: Dict):
    """Save complete analysis result."""
    ensure_storage()
    
    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)
    
    result['analyzed_at'] = datetime.utcnow().isoformat()
    data[channel_id] = result
    
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_analysis_result(channel_id: str) -> Optional[Dict]:
    """Retrieve analysis result for a channel."""
    ensure_storage()
    
    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)
    
    return data.get(channel_id)


def save_historical_accuracy(channel_id: str, accuracy: float):
    """Save/update historical accuracy for an influencer."""
    ensure_storage()
    
    with open(ACCURACY_FILE, 'r') as f:
        data = json.load(f)
    
    data[channel_id] = {
        'accuracy': accuracy,
        'updated_at': datetime.utcnow().isoformat()
    }
    
    with open(ACCURACY_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_historical_accuracy(channel_id: str) -> float:
    """Get historical accuracy for an influencer. Defaults to 50 if not set."""
    ensure_storage()
    
    with open(ACCURACY_FILE, 'r') as f:
        data = json.load(f)
    
    if channel_id in data:
        return data[channel_id]['accuracy']
    
    # Default: neutral accuracy if no data
    return 50.0


def list_all_analyses() -> Dict:
    """List all stored analyses."""
    ensure_storage()
    
    with open(RESULTS_FILE, 'r') as f:
        return json.load(f)