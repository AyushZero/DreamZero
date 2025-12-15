"""
Configuration settings for Dream Journal Emotion Tracker
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dream-journal-secret-key-2025'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///dream_journal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    ENTRIES_PER_PAGE = 10
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # NLP settings
    EMOTION_CATEGORIES = [
        'joy', 'sadness', 'fear', 'anger', 
        'surprise', 'disgust', 'trust', 'anticipation'
    ]
    
    # Visualization settings
    DASHBOARD_THEME = 'plotly_white'
    COLOR_SCHEME = {
        'joy': '#FFD700',
        'sadness': '#4169E1',
        'fear': '#8B008B',
        'anger': '#DC143C',
        'surprise': '#FF69B4',
        'disgust': '#556B2F',
        'trust': '#00CED1',
        'anticipation': '#FFA500'
    }
    
    # Privacy settings
    LOCAL_PROCESSING = True  # All NLP processing happens locally
    ENABLE_EXPORT = True
    ENABLE_SHARING = False  # Can be enabled later for community features
    
    # Reminder settings
    ENABLE_REMINDERS = True
    DEFAULT_REMINDER_TIME = "08:00"  # Morning reminder
