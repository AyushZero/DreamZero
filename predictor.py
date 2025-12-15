"""
Prediction and insights generation module
Analyzes historical dream data to predict patterns and provide insights
"""
from datetime import datetime, timedelta
from collections import Counter
import json
import numpy as np
from models import DreamEntry
from sklearn.linear_model import LinearRegression


class DreamPredictor:
    """Generate predictions and insights from dream data"""
    
    def __init__(self):
        self.model = LinearRegression()
    
    def predict_mood_trend(self, entries, days_ahead=7):
        """
        Predict sentiment trend for the next N days
        Returns predicted sentiment scores
        """
        if len(entries) < 7:
            return None
        
        # Prepare data
        dates = []
        sentiments = []
        
        for entry in sorted(entries, key=lambda x: x.dream_date):
            if entry.sentiment_score is not None:
                days_from_start = (entry.dream_date - entries[0].dream_date).days
                dates.append(days_from_start)
                sentiments.append(entry.sentiment_score)
        
        if len(dates) < 3:
            return None
        
        # Fit linear regression
        X = np.array(dates).reshape(-1, 1)
        y = np.array(sentiments)
        
        try:
            self.model.fit(X, y)
            
            # Predict future values
            last_day = dates[-1]
            future_days = [last_day + i for i in range(1, days_ahead + 1)]
            predictions = self.model.predict(np.array(future_days).reshape(-1, 1))
            
            return {
                'days': future_days,
                'predictions': [float(p) for p in predictions],
                'trend': 'improving' if predictions[-1] > predictions[0] else 'declining',
                'confidence': 'low' if len(dates) < 14 else 'medium' if len(dates) < 30 else 'high'
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def identify_patterns(self, entries):
        """
        Identify recurring patterns in dreams
        Returns insights about dream patterns
        """
        patterns = {
            'time_of_day': self._analyze_time_patterns(entries),
            'day_of_week': self._analyze_day_patterns(entries),
            'emotion_correlations': self._analyze_emotion_correlations(entries),
            'sleep_quality_impact': self._analyze_sleep_quality(entries),
            'cyclical_themes': self._analyze_cyclical_themes(entries)
        }
        
        return patterns
    
    def _analyze_time_patterns(self, entries):
        """Analyze if certain times of day correlate with dream types"""
        morning_dreams = []
        evening_dreams = []
        
        for entry in entries:
            hour = entry.dream_date.hour
            
            if hour < 12:
                morning_dreams.append(entry.sentiment_score)
            else:
                evening_dreams.append(entry.sentiment_score)
        
        if morning_dreams and evening_dreams:
            return {
                'morning_avg': sum(morning_dreams) / len(morning_dreams),
                'evening_avg': sum(evening_dreams) / len(evening_dreams),
                'insight': 'Morning dreams tend to be more positive' 
                    if sum(morning_dreams) / len(morning_dreams) > sum(evening_dreams) / len(evening_dreams)
                    else 'Evening dreams tend to be more positive'
            }
        
        return None
    
    def _analyze_day_patterns(self, entries):
        """Analyze dream patterns by day of week"""
        day_sentiments = {i: [] for i in range(7)}
        
        for entry in entries:
            day = entry.dream_date.weekday()
            if entry.sentiment_score is not None:
                day_sentiments[day].append(entry.sentiment_score)
        
        day_averages = {
            day: sum(scores) / len(scores) if scores else None
            for day, scores in day_sentiments.items()
        }
        
        # Find best and worst days
        valid_days = {k: v for k, v in day_averages.items() if v is not None}
        if not valid_days:
            return None
        
        days_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        best_day = max(valid_days.items(), key=lambda x: x[1])
        worst_day = min(valid_days.items(), key=lambda x: x[1])
        
        return {
            'best_day': days_names[best_day[0]],
            'best_score': best_day[1],
            'worst_day': days_names[worst_day[0]],
            'worst_score': worst_day[1],
            'insight': f"Dreams on {days_names[best_day[0]]} tend to be most positive"
        }
    
    def _analyze_emotion_correlations(self, entries):
        """Find correlations between different emotions"""
        # This is simplified - in production, use proper correlation analysis
        emotion_pairs = []
        
        for entry in entries:
            if entry.emotions:
                emotions = json.loads(entry.emotions)
                top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:2]
                if len(top_emotions) == 2 and top_emotions[1][1] > 0.1:
                    pair = tuple(sorted([top_emotions[0][0], top_emotions[1][0]]))
                    emotion_pairs.append(pair)
        
        if emotion_pairs:
            most_common = Counter(emotion_pairs).most_common(3)
            return {
                'common_pairs': [
                    {'emotions': list(pair), 'frequency': count}
                    for pair, count in most_common
                ],
                'insight': f"{most_common[0][0][0]} and {most_common[0][0][1]} often appear together"
                    if most_common else 'No clear emotion patterns found'
            }
        
        return None
    
    def _analyze_sleep_quality(self, entries):
        """Analyze impact of sleep quality on dream sentiment"""
        quality_sentiments = {}
        
        for entry in entries:
            if entry.sleep_quality and entry.sentiment_score is not None:
                quality = entry.sleep_quality
                if quality not in quality_sentiments:
                    quality_sentiments[quality] = []
                quality_sentiments[quality].append(entry.sentiment_score)
        
        if len(quality_sentiments) < 3:
            return None
        
        # Calculate averages
        quality_averages = {
            q: sum(scores) / len(scores)
            for q, scores in quality_sentiments.items()
        }
        
        # Check correlation
        qualities = list(quality_averages.keys())
        sentiments = [quality_averages[q] for q in qualities]
        
        # Simple correlation check
        correlation = np.corrcoef(qualities, sentiments)[0, 1] if len(qualities) > 1 else 0
        
        return {
            'correlation': float(correlation),
            'insight': 'Better sleep quality correlates with more positive dreams' 
                if correlation > 0.3 
                else 'No clear correlation between sleep quality and dream sentiment'
                if abs(correlation) < 0.3
                else 'Paradoxically, lower sleep quality shows more positive dreams'
        }
    
    def _analyze_cyclical_themes(self, entries):
        """Detect if certain themes appear in cycles"""
        # Track themes over time
        theme_timeline = {}
        
        for entry in sorted(entries, key=lambda x: x.dream_date):
            if entry.themes:
                themes = json.loads(entry.themes)
                date = entry.dream_date.date()
                
                for theme in themes:
                    if theme not in theme_timeline:
                        theme_timeline[theme] = []
                    theme_timeline[theme].append(date)
        
        # Find themes with regular intervals
        cyclical_themes = []
        
        for theme, dates in theme_timeline.items():
            if len(dates) >= 3:
                # Calculate intervals between occurrences
                intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
                if intervals:
                    avg_interval = sum(intervals) / len(intervals)
                    
                    # Check if intervals are relatively consistent
                    variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals)
                    if variance < avg_interval * 0.5:  # Low variance = cyclical
                        cyclical_themes.append({
                            'theme': theme,
                            'avg_interval_days': round(avg_interval, 1),
                            'occurrences': len(dates)
                        })
        
        if cyclical_themes:
            return {
                'themes': cyclical_themes,
                'insight': f"Theme '{cyclical_themes[0]['theme']}' appears every ~{cyclical_themes[0]['avg_interval_days']} days"
                    if cyclical_themes else 'No clear cyclical themes detected'
            }
        
        return None
    
    def generate_personalized_insights(self, entries):
        """
        Generate personalized insights and recommendations
        """
        if len(entries) < 5:
            return {
                'message': 'Keep recording your dreams! We need more data to generate personalized insights.',
                'tips': [
                    'Try to record dreams immediately upon waking',
                    'Include as many details as possible',
                    'Note your sleep quality and mood'
                ]
            }
        
        insights = []
        recommendations = []
        
        # Analyze recent trend
        recent_entries = sorted(entries, key=lambda x: x.dream_date)[-7:]
        recent_sentiment = sum(e.sentiment_score for e in recent_entries if e.sentiment_score) / len(recent_entries)
        
        if recent_sentiment < -0.3:
            insights.append("Your recent dreams show negative sentiment patterns")
            recommendations.append("Consider stress-reduction techniques before bed")
            recommendations.append("Try journaling worries before sleep")
        elif recent_sentiment > 0.3:
            insights.append("Your recent dreams are predominantly positive!")
            recommendations.append("Continue your current sleep routine")
        
        # Analyze stress levels
        recent_stress = sum(e.stress_level for e in recent_entries if e.stress_level) / len(recent_entries)
        if recent_stress > 0.6:
            insights.append("High stress indicators detected in your dreams")
            recommendations.append("Practice relaxation exercises before bed")
            recommendations.append("Reduce screen time in the evening")
        
        # Check for recurring nightmares
        nightmare_count = sum(1 for e in recent_entries if e.sentiment_score and e.sentiment_score < -0.5)
        if nightmare_count >= 3:
            insights.append(f"You've had {nightmare_count} nightmares in the past week")
            recommendations.append("Consider speaking with a healthcare professional if nightmares persist")
        
        # Analyze dream frequency
        date_range = (entries[-1].dream_date - entries[0].dream_date).days
        frequency = len(entries) / max(date_range, 1) * 7
        
        if frequency < 2:
            insights.append("You're recording dreams infrequently")
            recommendations.append("Try setting a morning reminder to record dreams")
        elif frequency > 5:
            insights.append("Excellent dream recall! You're recording frequently")
            recommendations.append("Your detailed records will provide rich insights")
        
        return {
            'insights': insights,
            'recommendations': recommendations,
            'stats': {
                'total_dreams': len(entries),
                'avg_sentiment': sum(e.sentiment_score for e in entries if e.sentiment_score) / len(entries),
                'dreams_per_week': round(frequency, 1),
                'recent_stress': round(recent_stress, 2)
            }
        }
