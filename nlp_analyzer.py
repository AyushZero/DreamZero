"""
NLP Analysis Engine for Dream Journal
Performs sentiment analysis, emotion detection, entity extraction, and theme identification
"""
import re
import json
from collections import Counter
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from config import Config

class DreamAnalyzer:
    """Main NLP analyzer for dream entries"""
    
    def __init__(self):
        """Initialize NLP models and analyzers"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spacy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        self.vader = SentimentIntensityAnalyzer()
        
        # Emotion lexicon (simplified - can be expanded)
        self.emotion_keywords = {
            'joy': ['happy', 'joyful', 'excited', 'delighted', 'cheerful', 'wonderful', 
                    'amazing', 'love', 'loved', 'beautiful', 'peaceful', 'content'],
            'sadness': ['sad', 'unhappy', 'depressed', 'lonely', 'crying', 'tears', 
                       'grief', 'loss', 'heartbroken', 'miserable', 'gloomy'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'worried', 'panic', 
                    'nightmare', 'horror', 'frightened', 'threatened', 'danger'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'frustrated', 'irritated', 
                     'annoyed', 'hostile', 'aggressive', 'violent'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 
                        'unexpected', 'sudden', 'startled'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'nasty', 'gross', 
                       'horrible', 'awful', 'unpleasant'],
            'trust': ['trust', 'safe', 'secure', 'comfortable', 'protected', 
                     'confident', 'reliable'],
            'anticipation': ['waiting', 'expecting', 'anticipating', 'looking forward', 
                           'preparing', 'ready', 'hopeful']
        }
        
        # Stress indicators
        self.stress_keywords = [
            'chased', 'running', 'late', 'test', 'exam', 'unprepared', 
            'falling', 'drowning', 'trapped', 'lost', 'naked', 'public',
            'teeth falling', 'unable to move', 'paralyzed', 'screaming'
        ]
    
    def analyze_dream(self, content):
        """
        Perform comprehensive analysis on dream content
        Returns dict with sentiment, emotions, entities, themes, intensity, stress level
        """
        if not content or not content.strip():
            return self._empty_analysis()
        
        # Perform all analyses
        sentiment = self._analyze_sentiment(content)
        emotions = self._detect_emotions(content)
        entities = self._extract_entities(content)
        themes = self._identify_themes(content)
        intensity = self._calculate_intensity(content, emotions)
        stress_level = self._detect_stress(content)
        
        return {
            'sentiment_score': sentiment,
            'emotions': emotions,
            'entities': entities,
            'themes': themes,
            'dream_intensity': intensity,
            'stress_level': stress_level
        }
    
    def _analyze_sentiment(self, text):
        """
        Analyze sentiment using VADER and TextBlob
        Returns score from -1 (negative) to 1 (positive)
        """
        # VADER sentiment
        vader_scores = self.vader.polarity_scores(text)
        vader_compound = vader_scores['compound']
        
        # TextBlob sentiment
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        
        # Average both methods
        sentiment = (vader_compound + textblob_polarity) / 2
        return round(sentiment, 3)
    
    def _detect_emotions(self, text):
        """
        Detect emotions using keyword matching
        Returns dict of emotion scores
        """
        text_lower = text.lower()
        doc = self.nlp(text)
        word_count = len([token for token in doc if not token.is_stop and not token.is_punct])
        
        if word_count == 0:
            word_count = 1  # Avoid division by zero
        
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            # Normalize by word count
            score = min(matches / (word_count * 0.1), 1.0)  # Cap at 1.0
            emotion_scores[emotion] = round(score, 3)
        
        return emotion_scores
    
    def _extract_entities(self, text):
        """
        Extract named entities (people, places, objects)
        Returns dict categorized by entity type
        """
        doc = self.nlp(text)
        
        entities = {
            'people': [],
            'places': [],
            'organizations': [],
            'other': []
        }
        
        for ent in doc.ents:
            entity_text = ent.text.strip()
            if ent.label_ == 'PERSON':
                entities['people'].append(entity_text)
            elif ent.label_ in ['GPE', 'LOC', 'FAC']:
                entities['places'].append(entity_text)
            elif ent.label_ == 'ORG':
                entities['organizations'].append(entity_text)
            else:
                entities['other'].append(entity_text)
        
        # Extract common nouns as potential dream symbols
        nouns = [token.text.lower() for token in doc 
                if token.pos_ == 'NOUN' and not token.is_stop and len(token.text) > 3]
        entities['symbols'] = list(set(nouns[:10]))  # Top 10 unique nouns
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _identify_themes(self, text):
        """
        Identify recurring themes based on content analysis
        Returns list of theme keywords
        """
        doc = self.nlp(text)
        
        # Extract noun chunks as potential themes
        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        
        # Common dream themes
        common_themes = {
            'flying': ['flying', 'floating', 'soaring', 'air'],
            'falling': ['falling', 'dropping', 'plunging'],
            'chase': ['chased', 'running from', 'pursued', 'escape'],
            'water': ['water', 'ocean', 'sea', 'river', 'swimming', 'drowning'],
            'death': ['death', 'dying', 'dead', 'funeral'],
            'school': ['school', 'class', 'teacher', 'exam', 'test'],
            'work': ['work', 'office', 'boss', 'job', 'meeting'],
            'family': ['family', 'mother', 'father', 'parent', 'sibling'],
            'romance': ['love', 'kiss', 'romantic', 'date', 'partner'],
            'animals': ['dog', 'cat', 'animal', 'bird', 'snake'],
            'travel': ['travel', 'journey', 'trip', 'destination'],
            'home': ['home', 'house', 'room', 'apartment']
        }
        
        identified_themes = []
        text_lower = text.lower()
        
        for theme, keywords in common_themes.items():
            if any(keyword in text_lower for keyword in keywords):
                identified_themes.append(theme)
        
        return identified_themes
    
    def _calculate_intensity(self, text, emotions):
        """
        Calculate dream intensity based on content and emotions
        Returns score from 0 to 1
        """
        # Factors: word count, exclamation marks, emotional words
        word_count = len(text.split())
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        # Emotional intensity (sum of all emotion scores)
        emotion_intensity = sum(emotions.values())
        
        # Normalize intensity
        intensity = min(
            (word_count / 500) * 0.3 +  # Longer dreams get higher intensity
            (exclamation_count / 10) * 0.2 +
            (question_count / 10) * 0.1 +
            emotion_intensity * 0.4,
            1.0
        )
        
        return round(intensity, 3)
    
    def _detect_stress(self, text):
        """
        Detect stress indicators in dream content
        Returns stress level from 0 to 1
        """
        text_lower = text.lower()
        
        # Count stress keywords
        stress_matches = sum(1 for keyword in self.stress_keywords if keyword in text_lower)
        
        # Check for negative sentiment
        sentiment = self._analyze_sentiment(text)
        negative_sentiment = max(0, -sentiment)
        
        # Combine factors
        stress_level = min(
            (stress_matches / 5) * 0.6 +  # Stress keywords
            negative_sentiment * 0.4,      # Negative sentiment
            1.0
        )
        
        return round(stress_level, 3)
    
    def _empty_analysis(self):
        """Return empty analysis results"""
        return {
            'sentiment_score': 0.0,
            'emotions': {emotion: 0.0 for emotion in Config.EMOTION_CATEGORIES},
            'entities': {'people': [], 'places': [], 'organizations': [], 'other': [], 'symbols': []},
            'themes': [],
            'dream_intensity': 0.0,
            'stress_level': 0.0
        }
    
    def generate_insights(self, entries):
        """
        Generate insights from multiple dream entries
        Used for weekly/monthly summaries
        """
        if not entries:
            return None
        
        total = len(entries)
        avg_sentiment = sum(e.sentiment_score for e in entries if e.sentiment_score) / total
        
        # Aggregate emotions
        all_emotions = {}
        for entry in entries:
            if entry.emotions:
                emotions = json.loads(entry.emotions)
                for emotion, score in emotions.items():
                    all_emotions[emotion] = all_emotions.get(emotion, 0) + score
        
        # Find dominant emotion
        dominant_emotion = max(all_emotions.items(), key=lambda x: x[1])[0] if all_emotions else 'neutral'
        
        # Normalize emotion distribution
        emotion_total = sum(all_emotions.values())
        emotion_distribution = {
            emotion: round(score / emotion_total, 3) 
            for emotion, score in all_emotions.items()
        } if emotion_total > 0 else {}
        
        # Aggregate themes
        all_themes = []
        for entry in entries:
            if entry.themes:
                all_themes.extend(json.loads(entry.themes))
        recurring_themes = [theme for theme, count in Counter(all_themes).most_common(5)]
        
        # Stress trend analysis
        stress_levels = [e.stress_level for e in entries if e.stress_level is not None]
        if len(stress_levels) >= 2:
            first_half = sum(stress_levels[:len(stress_levels)//2]) / (len(stress_levels)//2)
            second_half = sum(stress_levels[len(stress_levels)//2:]) / (len(stress_levels) - len(stress_levels)//2)
            
            if second_half > first_half * 1.1:
                stress_trend = 'increasing'
            elif second_half < first_half * 0.9:
                stress_trend = 'decreasing'
            else:
                stress_trend = 'stable'
        else:
            stress_trend = 'insufficient data'
        
        return {
            'total_entries': total,
            'avg_sentiment': round(avg_sentiment, 3),
            'dominant_emotion': dominant_emotion,
            'emotion_distribution': emotion_distribution,
            'recurring_themes': recurring_themes,
            'stress_trend': stress_trend
        }
