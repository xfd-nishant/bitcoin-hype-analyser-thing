"""
Metric extraction engine for credibility analysis.
Converts transcript text into quantified metrics.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class MetricsExtractor:
    """Extracts credibility metrics from transcript text."""
    
    # Emotional intensity markers
    INTENSITY_WORDS = {
        'massive', 'explosive', 'crash', 'moon', 'guaranteed', 'insane', 
        'never', 'always', 'huge', 'enormous', 'catastrophic', 'incredible',
        'unbelievable', 'shocking', 'extreme', 'violent', 'brutal', 'devastating',
        'parabolic', 'exponential', 'rocket', 'skyrocket', 'plummet', 'collapse'
    }
    
    # High certainty markers
    HIGH_CERTAINTY = {
        'will', 'guaranteed', 'definitely', 'certain', 'surely', 'absolutely',
        'without doubt', 'no doubt', '100%', 'must', 'inevitable', 'obviously'
    }
    
    # Hedge words (uncertainty markers)
    HEDGE_WORDS = {
        'might', 'could', 'possibly', 'perhaps', 'maybe', 'probably',
        'likely', 'uncertain', 'unclear', 'potentially', 'may', 'seems',
        'appears', 'suggests', 'indicates', 'could be', 'might be'
    }
    
    # Technical crypto terms
    TECHNICAL_TERMS = {
        'on-chain', 'liquidity', 'derivatives', 'gamma', 'basis', 'arbitrage',
        'orderbook', 'order book', 'volatility', 'correlation', 'hedge',
        'futures', 'perpetual', 'funding rate', 'open interest', 'options',
        'delta', 'implied volatility', 'mark price', 'index price',
        'liquidation', 'leverage', 'margin', 'collateral', 'defi', 'tvl',
        'smart contract', 'validator', 'consensus', 'hash rate', 'difficulty',
        'mempool', 'block', 'transaction', 'gas', 'wei', 'gwei', 'slippage',
        'impermanent loss', 'yield farming', 'staking', 'proof of stake',
        'proof of work', 'eip', 'fork', 'halving', 'difficulty adjustment'
    }
    
    # Prediction patterns (regex)
    PREDICTION_PATTERNS = [
        r'\b(?:will|gonna|going to)\s+(?:hit|reach|go to|be|see)\s+[\$\d]',
        r'\$?\d+[kKmMbB]?\s+(?:by|before|within)\s+(?:next|the|end)',
        r'(?:bullish|bearish)\s+(?:for|on|into)\s+\d{4}',
        r'expect\s+\w+\s+to\s+(?:hit|reach|go)',
        r'predict\s+\w+\s+(?:will|to)',
        r'(?:we\'re|we are)\s+(?:going|headed)\s+(?:to|for|towards)'
    ]
    
    def __init__(self):
        pass
    
    def extract_all_metrics(self, transcript: str, metadata: Dict = None) -> Dict:
        """
        Extract all metrics from a transcript.
        
        Args:
            transcript: Full text transcript
            metadata: Optional video metadata (title, date, views)
            
        Returns:
            Dictionary containing all computed metrics
        """
        # Normalize text
        text_lower = transcript.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        word_count = len(words)
        
        # Extract each metric
        emotional_intensity = self._calculate_emotional_intensity(text_lower, word_count)
        certainty_index = self._calculate_certainty_index(text_lower)
        technical_depth = self._calculate_technical_depth(text_lower, word_count)
        prediction_density = self._calculate_prediction_density(transcript, word_count)
        
        # Extract evidence
        predictions = self._extract_predictions(transcript)
        intensity_quotes = self._extract_intensity_quotes(transcript)
        certainty_quotes = self._extract_certainty_quotes(transcript)
        technical_quotes = self._extract_technical_quotes(transcript)
        
        return {
            'metrics': {
                'emotional_intensity': round(emotional_intensity, 1),
                'certainty_index': round(certainty_index, 1),
                'technical_depth': round(technical_depth, 1),
                'prediction_density': round(prediction_density, 1),
                'word_count': word_count
            },
            'predictions': predictions,
            'evidence': {
                'intensity_quotes': intensity_quotes[:5],  # Top 5
                'certainty_quotes': certainty_quotes[:5],
                'technical_quotes': technical_quotes[:5]
            },
            'metadata': metadata or {}
        }
    
    def _calculate_emotional_intensity(self, text: str, word_count: int) -> float:
        """Calculate emotional intensity score (0-100)."""
        if word_count == 0:
            return 0.0
        
        # Count intensity words
        intensity_count = sum(1 for word in self.INTENSITY_WORDS if word in text)
        
        # Normalize per 1000 words
        per_1k = (intensity_count / word_count) * 1000
        
        # Scale to 0-100 (assume baseline 95th percentile is ~8 intensity words per 1k)
        baseline_95th = 8.0
        score = min(100, (per_1k / baseline_95th) * 100)
        
        return score
    
    def _calculate_certainty_index(self, text: str) -> float:
        """Calculate certainty index (0-100) based on certainty vs hedge ratio."""
        certainty_count = sum(1 for word in self.HIGH_CERTAINTY if word in text)
        hedge_count = sum(1 for word in self.HEDGE_WORDS if word in text)
        
        # Avoid division by zero
        if certainty_count + hedge_count == 0:
            return 50.0  # Neutral
        
        certainty_ratio = certainty_count / (certainty_count + hedge_count)
        return certainty_ratio * 100
    
    def _calculate_technical_depth(self, text: str, word_count: int) -> float:
        """Calculate technical depth score (0-100)."""
        if word_count == 0:
            return 0.0
        
        # Count unique technical terms used
        unique_terms = set()
        for term in self.TECHNICAL_TERMS:
            if term in text:
                unique_terms.add(term)
        
        # Density per 1000 words
        term_count = len(unique_terms)
        density = (term_count / word_count) * 1000
        
        # Scale (assume baseline median is ~10 terms per 1k words)
        baseline_median = 10.0
        score = min(100, (density / baseline_median) * 50)
        
        return score
    
    def _calculate_prediction_density(self, text: str, word_count: int) -> float:
        """Calculate prediction density score (0-100)."""
        if word_count == 0:
            return 0.0
        
        # Count prediction sentences
        prediction_count = 0
        for pattern in self.PREDICTION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            prediction_count += len(matches)
        
        # Normalize per 1000 words
        per_1k = (prediction_count / word_count) * 1000
        
        # Scale (5+ predictions per 1k = max score)
        score = min(100, (per_1k / 5.0) * 100)
        
        return score
    
    def _extract_predictions(self, text: str) -> List[str]:
        """Extract actual prediction sentences."""
        sentences = re.split(r'[.!?]+', text)
        predictions = []
        
        for sentence in sentences:
            for pattern in self.PREDICTION_PATTERNS:
                if re.search(pattern, sentence, re.IGNORECASE):
                    cleaned = sentence.strip()
                    if len(cleaned) > 20 and cleaned not in predictions:
                        predictions.append(cleaned)
                    break
        
        return predictions[:10]  # Return top 10
    
    def _extract_intensity_quotes(self, text: str) -> List[str]:
        """Extract sentences with high emotional intensity."""
        sentences = re.split(r'[.!?]+', text)
        quotes = []
        
        for sentence in sentences:
            lower = sentence.lower()
            intensity_count = sum(1 for word in self.INTENSITY_WORDS if word in lower)
            if intensity_count >= 2:  # At least 2 intensity words
                quotes.append(sentence.strip())
        
        return quotes
    
    def _extract_certainty_quotes(self, text: str) -> List[str]:
        """Extract sentences with high certainty language."""
        sentences = re.split(r'[.!?]+', text)
        quotes = []
        
        for sentence in sentences:
            lower = sentence.lower()
            certainty_count = sum(1 for word in self.HIGH_CERTAINTY if word in lower)
            if certainty_count >= 1:
                quotes.append(sentence.strip())
        
        return quotes
    
    def _extract_technical_quotes(self, text: str) -> List[str]:
        """Extract sentences with technical terms."""
        sentences = re.split(r'[.!?]+', text)
        quotes = []
        
        for sentence in sentences:
            lower = sentence.lower()
            term_count = sum(1 for term in self.TECHNICAL_TERMS if term in lower)
            if term_count >= 2:  # At least 2 technical terms
                quotes.append(sentence.strip())
        
        return quotes


def calculate_credibility_score(metrics: Dict, historical_accuracy: float) -> Dict:
    """
    Calculate composite credibility score.
    
    Args:
        metrics: Dictionary with emotional_intensity, certainty_index, technical_depth, prediction_density
        historical_accuracy: Historical accuracy score (0-100)
        
    Returns:
        Dictionary with credibility_score, calibration_gap, and flags
    """
    emotional = metrics['emotional_intensity']
    certainty = metrics['certainty_index']
    technical = metrics['technical_depth']
    pred_density = metrics['prediction_density']
    
    # Calculate calibration gap
    calibration_gap = certainty - historical_accuracy
    
    # Calibration penalty
    if calibration_gap > 30:
        calibration_penalty = 20
    elif calibration_gap > 15:
        calibration_penalty = 10
    else:
        calibration_penalty = 0
    
    # Composite score
    credibility_score = (
        historical_accuracy * 0.40 +
        (100 - emotional) * 0.25 +
        technical * 0.20 +
        (100 - abs(pred_density - 50)) * 0.15 -
        calibration_penalty
    )
    
    credibility_score = max(0, min(100, credibility_score))
    
    # Generate flags
    flags = {
        'high_hype_low_accuracy': emotional > 70 and historical_accuracy < 50,
        'overconfident': calibration_gap > 30,
        'technical_but_inaccurate': technical > 60 and historical_accuracy < 45,
        'hedges_appropriately': certainty < 40 and historical_accuracy > 60,
        'extreme_prediction_volume': pred_density > 80,
        'calm_and_accurate': emotional < 40 and historical_accuracy > 65
    }
    
    return {
        'credibility_score': round(credibility_score, 1),
        'calibration_gap': round(calibration_gap, 1),
        'calibration_penalty': calibration_penalty,
        'flags': flags
    }