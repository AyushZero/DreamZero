"""
Visualization utilities for creating charts and graphs
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from collections import Counter
import json
from config import Config


def create_emotion_timeline(entries):
    """Create timeline chart showing emotion trends over time"""
    if not entries:
        return None
    
    dates = []
    emotions_over_time = {emotion: [] for emotion in Config.EMOTION_CATEGORIES}
    sentiment_scores = []
    
    for entry in entries:
        dates.append(entry.dream_date)
        sentiment_scores.append(entry.sentiment_score or 0)
        
        if entry.emotions:
            emotions = json.loads(entry.emotions)
            for emotion in Config.EMOTION_CATEGORIES:
                emotions_over_time[emotion].append(emotions.get(emotion, 0))
        else:
            for emotion in Config.EMOTION_CATEGORIES:
                emotions_over_time[emotion].append(0)
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add emotion traces
    for emotion, scores in emotions_over_time.items():
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=scores,
                name=emotion.capitalize(),
                mode='lines+markers',
                line=dict(color=Config.COLOR_SCHEME.get(emotion, '#888888')),
                opacity=0.7
            ),
            secondary_y=False
        )
    
    # Add sentiment line
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=sentiment_scores,
            name='Overall Sentiment',
            mode='lines',
            line=dict(color='black', width=3, dash='dash'),
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title='Emotion Timeline',
        xaxis_title='Date',
        hovermode='x unified',
        template=Config.DASHBOARD_THEME,
        height=500
    )
    
    fig.update_yaxes(title_text="Emotion Score", secondary_y=False)
    fig.update_yaxes(title_text="Sentiment Score", secondary_y=True)
    
    return fig.to_json()


def create_emotion_distribution(entries):
    """Create pie chart showing emotion distribution"""
    if not entries:
        return None
    
    emotion_totals = {emotion: 0 for emotion in Config.EMOTION_CATEGORIES}
    
    for entry in entries:
        if entry.emotions:
            emotions = json.loads(entry.emotions)
            for emotion, score in emotions.items():
                if emotion in emotion_totals:
                    emotion_totals[emotion] += score
    
    # Filter out emotions with zero values
    emotion_totals = {k: v for k, v in emotion_totals.items() if v > 0}
    
    if not emotion_totals:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=[e.capitalize() for e in emotion_totals.keys()],
        values=list(emotion_totals.values()),
        marker=dict(colors=[Config.COLOR_SCHEME.get(e, '#888888') for e in emotion_totals.keys()]),
        hole=0.3
    )])
    
    fig.update_layout(
        title='Emotion Distribution',
        template=Config.DASHBOARD_THEME,
        height=400
    )
    
    return fig.to_json()


def create_calendar_heatmap(entries):
    """Create calendar heatmap showing dream frequency and intensity"""
    if not entries:
        return None
    
    # Group by date
    date_intensity = {}
    for entry in entries:
        date_str = entry.dream_date.strftime('%Y-%m-%d')
        intensity = entry.dream_intensity or 0
        
        if date_str in date_intensity:
            date_intensity[date_str] = max(date_intensity[date_str], intensity)
        else:
            date_intensity[date_str] = intensity
    
    dates = list(date_intensity.keys())
    intensities = list(date_intensity.values())
    
    fig = go.Figure(data=go.Scatter(
        x=dates,
        y=[1] * len(dates),
        mode='markers',
        marker=dict(
            size=20,
            color=intensities,
            colorscale='YlOrRd',
            showscale=True,
            colorbar=dict(title="Intensity"),
            cmin=0,
            cmax=1
        ),
        text=[f"Date: {d}<br>Intensity: {i:.2f}" for d, i in zip(dates, intensities)],
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Dream Activity Calendar',
        yaxis=dict(visible=False),
        xaxis_title='Date',
        template=Config.DASHBOARD_THEME,
        height=200
    )
    
    return fig.to_json()


def create_stress_trend(entries):
    """Create line chart showing stress level trends"""
    if not entries:
        return None
    
    dates = []
    stress_levels = []
    
    for entry in entries:
        if entry.stress_level is not None:
            dates.append(entry.dream_date)
            stress_levels.append(entry.stress_level)
    
    if not stress_levels:
        return None
    
    # Calculate moving average
    window = 7
    moving_avg = []
    for i in range(len(stress_levels)):
        start_idx = max(0, i - window + 1)
        avg = sum(stress_levels[start_idx:i+1]) / (i - start_idx + 1)
        moving_avg.append(avg)
    
    fig = go.Figure()
    
    # Raw stress levels
    fig.add_trace(go.Scatter(
        x=dates,
        y=stress_levels,
        name='Stress Level',
        mode='markers',
        marker=dict(color='rgba(255, 0, 0, 0.5)', size=8)
    ))
    
    # Moving average
    fig.add_trace(go.Scatter(
        x=dates,
        y=moving_avg,
        name=f'{window}-Day Average',
        mode='lines',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title='Stress Level Trend',
        xaxis_title='Date',
        yaxis_title='Stress Level',
        yaxis=dict(range=[0, 1]),
        template=Config.DASHBOARD_THEME,
        height=400
    )
    
    return fig.to_json()


def create_wordcloud_data(entries):
    """Generate word frequency data for word cloud"""
    if not entries:
        return None
    
    # Aggregate all symbols/entities
    all_words = []
    
    for entry in entries:
        if entry.entities:
            entities = json.loads(entry.entities)
            all_words.extend(entities.get('symbols', []))
            all_words.extend(entities.get('people', []))
            all_words.extend(entities.get('places', []))
    
    # Count frequencies
    word_freq = Counter(all_words)
    
    # Return top 50 words
    return [
        {'text': word, 'value': count}
        for word, count in word_freq.most_common(50)
    ]


def create_sentiment_gauge(avg_sentiment):
    """Create gauge chart for overall sentiment"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_sentiment,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Sentiment"},
        delta={'reference': 0},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.3], 'color': "lightcoral"},
                {'range': [-0.3, 0.3], 'color': "lightyellow"},
                {'range': [0.3, 1], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0
            }
        }
    ))
    
    fig.update_layout(
        template=Config.DASHBOARD_THEME,
        height=300
    )
    
    return fig.to_json()


def create_theme_bar_chart(entries):
    """Create bar chart of recurring themes"""
    if not entries:
        return None
    
    all_themes = []
    for entry in entries:
        if entry.themes:
            all_themes.extend(json.loads(entry.themes))
    
    if not all_themes:
        return None
    
    theme_counts = Counter(all_themes)
    top_themes = theme_counts.most_common(10)
    
    themes, counts = zip(*top_themes) if top_themes else ([], [])
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(themes),
            y=list(counts),
            marker_color='indianred'
        )
    ])
    
    fig.update_layout(
        title='Top Dream Themes',
        xaxis_title='Theme',
        yaxis_title='Frequency',
        template=Config.DASHBOARD_THEME,
        height=400
    )
    
    return fig.to_json()
