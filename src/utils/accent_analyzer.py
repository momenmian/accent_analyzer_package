import os
import re
from typing import Dict, Any, Tuple

class AccentAnalyzer:
    """
    Class to analyze accents using pure Python (no native dependencies)
    """
    def __init__(self):
        """
        Initialize the accent analyzer
        """
        # Define accent characteristics for classification
        self.accent_characteristics = {
            "british": {
                "phonetic_patterns": [
                    r'\b(wa|o)ter\b',  # water with British pronunciation
                    r'\btoma(to|toes)\b',  # tomato with British pronunciation
                    r'\bschedule\b',  # schedule with British pronunciation
                    r'\bvitamin\b',  # vitamin with British pronunciation
                    r'\bmobile\b',  # mobile with British pronunciation
                ],
                "vocabulary": [
                    r'\blift\b', r'\bflat\b', r'\blorry\b', r'\bboot\b', r'\bqueue\b', r'\brubbish\b',
                    r'\bwhilst\b', r'\bautumn\b', r'\bholiday\b', r'\bpetrol\b', r'\bmotorway\b', r'\btrainers\b',
                    r'\bcolour\b', r'\bfavourite\b', r'\bcentre\b', r'\btheatre\b', r'\bspecialise\b', r'\borganise\b'
                ],
                "grammar": [
                    r'\bhave got\b', r'\bat the weekend\b', r'\bin hospital\b', r'\bat university\b',
                    r'\bdifferent to\b', r'\bwrite to\b', r'\btowards\b', r'\bI shall\b', r'\bI shan\'t\b'
                ]
            },
            "american": {
                "phonetic_patterns": [
                    r'\bwa(d|t)er\b',  # water with American pronunciation
                    r'\btomato\b',  # tomato with American pronunciation
                    r'\bschedule\b',  # schedule with American pronunciation
                    r'\bvitamin\b',  # vitamin with American pronunciation
                    r'\bmobile\b',  # mobile with American pronunciation
                ],
                "vocabulary": [
                    r'\belevator\b', r'\bapartment\b', r'\btruck\b', r'\btrunk\b', r'\bline\b', r'\btrash\b',
                    r'\bfall\b', r'\bvacation\b', r'\bgas\b', r'\bhighway\b', r'\bsneakers\b', r'\bsidewalk\b',
                    r'\bcolor\b', r'\bfavorite\b', r'\bcenter\b', r'\btheater\b', r'\bspecialize\b', r'\borganize\b'
                ],
                "grammar": [
                    r'\bhave gotten\b', r'\bon the weekend\b', r'\bin the hospital\b', r'\bin college\b',
                    r'\bdifferent from\b', r'\bwrite\b', r'\btoward\b', r'\bI will\b', r'\bI won\'t\b'
                ]
            },
            "australian": {
                "phonetic_patterns": [
                    r'\bd(a|i)y\b',  # day with Australian pronunciation
                    r'\bt(o|u)night\b',  # tonight with Australian pronunciation
                    r'\bm(a|i)te\b',  # mate with Australian pronunciation
                    r'\bh(e|i)re\b',  # here with Australian pronunciation
                    r'\bn(o|u)w\b',  # now with Australian pronunciation
                ],
                "vocabulary": [
                    r'\barvo\b', r'\bbarbie\b', r'\bbrekkie\b', r'\bute\b', r'\bthongs\b', r'\bservo\b',
                    r'\bmate\b', r'\bg\'day\b', r'\bfair dinkum\b', r'\bbloke\b', r'\bsheila\b', r'\bdunny\b',
                    r'\bsunnies\b', r'\btelly\b', r'\bbiscuit\b', r'\bchook\b', r'\bfooty\b', r'\bsanger\b'
                ],
                "grammar": [
                    r'\byeah\?$', r'\bie\b', r'\by\b', r'\bheaps\b', r'\breckon\b', r'\bno worries\b',
                    r'\bhow ya going\b', r'\btoo easy\b', r'\bshe\'ll be right\b', r'\bcrikey\b'
                ]
            }
        }
    
    def analyze_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Analyze audio file for accent detection
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            Dict[str, Any]: Analysis results including accent classification and confidence
        """
        # For demonstration purposes, we'll use a mock transcript
        # In a real implementation, you would use a pure Python speech recognition library
        # or a web API to transcribe the audio
        transcript = "This is a demonstration of accent analysis. The speaker is talking about various topics."
        
        # Analyze accent
        accent_classification, confidence, explanation = self._analyze_accent(transcript)
        
        return {
            "transcript": transcript,
            "accent_classification": accent_classification,
            "confidence_score": confidence,
            "explanation": explanation
        }
    
    def _analyze_accent(self, transcript: str) -> Tuple[str, float, str]:
        """
        Analyze accent using pattern matching
        
        Args:
            transcript (str): Transcribed text
            
        Returns:
            Tuple[str, float, str]: Accent classification, confidence score, and explanation
        """
        # Count occurrences of accent-specific patterns
        accent_scores = {
            "british": 0,
            "american": 0,
            "australian": 0
        }
        
        # Normalize transcript
        transcript_lower = transcript.lower()
        
        # Check for vocabulary, grammar, and phonetic patterns
        for accent, features in self.accent_characteristics.items():
            # Check vocabulary
            for pattern in features["vocabulary"]:
                matches = re.findall(pattern, transcript_lower, re.IGNORECASE)
                accent_scores[accent] += len(matches) * 2
            
            # Check grammar patterns
            for pattern in features["grammar"]:
                matches = re.findall(pattern, transcript_lower, re.IGNORECASE)
                accent_scores[accent] += len(matches) * 3
            
            # Check phonetic patterns
            for pattern in features["phonetic_patterns"]:
                matches = re.findall(pattern, transcript_lower, re.IGNORECASE)
                accent_scores[accent] += len(matches) * 2
        
        # Determine the most likely accent
        if sum(accent_scores.values()) > 0:
            # Normalize scores
            total_score = sum(accent_scores.values())
            for accent in accent_scores:
                accent_scores[accent] /= total_score
            
            # Get the accent with the highest score
            accent = max(accent_scores, key=accent_scores.get)
            confidence = accent_scores[accent]
        else:
            # Default to American with low confidence if no patterns detected
            accent = "american"
            confidence = 0.4
        
        # Generate explanation
        explanation = self._generate_explanation(transcript, accent, confidence)
        
        return accent, confidence, explanation
    
    def _generate_explanation(self, transcript: str, accent: str, confidence: float) -> str:
        """
        Generate explanation for accent classification
        
        Args:
            transcript (str): Transcribed text
            accent (str): Classified accent
            confidence (float): Confidence score
            
        Returns:
            str: Explanation
        """
        # Start with basic explanation
        explanation = f"The speaker's accent is classified as {accent.capitalize()} with {confidence*100:.1f}% confidence. "
        
        # Add details based on the accent
        if accent == "british":
            explanation += "British English speakers typically use non-rhotic pronunciation (dropping the 'r' sound after vowels) and have distinct vocabulary such as 'lift' instead of 'elevator'."
        elif accent == "american":
            explanation += "American English speakers typically use rhotic pronunciation (pronouncing the 'r' sound after vowels) and have distinct vocabulary such as 'elevator' instead of 'lift'."
        elif accent == "australian":
            explanation += "Australian English speakers often have a distinctive rising intonation at the end of sentences and use unique vocabulary and expressions."
        
        # Add confidence qualifier
        if confidence < 0.5:
            explanation += " However, the confidence is relatively low, so this classification should be considered tentative."
        
        return explanation
