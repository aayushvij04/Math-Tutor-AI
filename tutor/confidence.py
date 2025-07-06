from typing import List
from transformers import pipeline

class ConfidenceChecker:
    def __init__(self):
        self.keywords = [
            "i can't", "i cannot", "i'm stuck", "i give up", "this is hard", "i don't get it", "i am confused", "i'm lost"
        ]
        self.sentiment = pipeline('sentiment-analysis')

    def is_low_confidence(self, user_input: str) -> bool:
        text = user_input.lower()
        if any(kw in text for kw in self.keywords):
            return True
        # Use sentiment model (negative/neutral = low confidence)
        result = self.sentiment(user_input)[0]
        if result['label'] == 'NEGATIVE' or (result['label'] == 'NEUTRAL' and result['score'] > 0.7):
            return True
        return False 