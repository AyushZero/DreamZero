"""
Database models for Dream Journal
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class DreamEntry(db.Model):
    """Model for storing dream journal entries"""
    __tablename__ = 'dream_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    dream_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User-added metadata
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    sleep_quality = db.Column(db.Integer, nullable=True)  # 1-10 scale
    
    # Analysis results (stored as JSON)
    sentiment_score = db.Column(db.Float, nullable=True)  # -1 to 1
    emotions = db.Column(db.Text, nullable=True)  # JSON: emotion scores
    entities = db.Column(db.Text, nullable=True)  # JSON: people, places, objects
    themes = db.Column(db.Text, nullable=True)  # JSON: recurring themes
    
    # Computed metrics
    dream_intensity = db.Column(db.Float, nullable=True)  # 0-1 scale
    stress_level = db.Column(db.Float, nullable=True)  # 0-1 scale
    
    def __repr__(self):
        return f'<DreamEntry {self.id}: {self.title or "Untitled"}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'dream_date': self.dream_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': self.tags.split(',') if self.tags else [],
            'sleep_quality': self.sleep_quality,
            'sentiment_score': self.sentiment_score,
            'emotions': json.loads(self.emotions) if self.emotions else {},
            'entities': json.loads(self.entities) if self.entities else {},
            'themes': json.loads(self.themes) if self.themes else [],
            'dream_intensity': self.dream_intensity,
            'stress_level': self.stress_level
        }
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()] if self.tags else []
    
    def set_tags_list(self, tags_list):
        """Set tags from a list"""
        self.tags = ','.join(tags_list) if tags_list else None


class EmotionSummary(db.Model):
    """Model for storing periodic emotion summaries"""
    __tablename__ = 'emotion_summaries'
    
    id = db.Column(db.Integer, primary_key=True)
    period_type = db.Column(db.String(20), nullable=False)  # 'weekly', 'monthly'
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Summary statistics
    total_entries = db.Column(db.Integer, nullable=False, default=0)
    avg_sentiment = db.Column(db.Float, nullable=True)
    dominant_emotion = db.Column(db.String(50), nullable=True)
    emotion_distribution = db.Column(db.Text, nullable=True)  # JSON
    
    # Insights
    recurring_themes = db.Column(db.Text, nullable=True)  # JSON
    common_entities = db.Column(db.Text, nullable=True)  # JSON
    stress_trend = db.Column(db.String(20), nullable=True)  # 'increasing', 'decreasing', 'stable'
    
    # AI-generated insights
    summary_text = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<EmotionSummary {self.period_type} {self.period_start}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'period_type': self.period_type,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'created_at': self.created_at.isoformat(),
            'total_entries': self.total_entries,
            'avg_sentiment': self.avg_sentiment,
            'dominant_emotion': self.dominant_emotion,
            'emotion_distribution': json.loads(self.emotion_distribution) if self.emotion_distribution else {},
            'recurring_themes': json.loads(self.recurring_themes) if self.recurring_themes else [],
            'common_entities': json.loads(self.common_entities) if self.common_entities else {},
            'stress_trend': self.stress_trend,
            'summary_text': self.summary_text,
            'recommendations': self.recommendations
        }
