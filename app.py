"""
Flask Application - Dream Journal Emotion Tracker
Main application with API endpoints
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db, DreamEntry, EmotionSummary
from nlp_analyzer import DreamAnalyzer
from config import Config
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize NLP analyzer
analyzer = DreamAnalyzer()

# Create database tables
with app.app_context():
    db.create_all()


# ============= API ENDPOINTS =============

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all dream entries with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', Config.ENTRIES_PER_PAGE, type=int)
    
    # Optional filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    tag = request.args.get('tag')
    
    query = DreamEntry.query.order_by(DreamEntry.dream_date.desc())
    
    # Apply filters
    if start_date:
        query = query.filter(DreamEntry.dream_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(DreamEntry.dream_date <= datetime.fromisoformat(end_date))
    if tag:
        query = query.filter(DreamEntry.tags.like(f'%{tag}%'))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'entries': [entry.to_dict() for entry in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    """Get a specific dream entry"""
    entry = DreamEntry.query.get_or_404(entry_id)
    return jsonify(entry.to_dict())


@app.route('/api/entries', methods=['POST'])
def create_entry():
    """Create a new dream entry with NLP analysis"""
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    # Create new entry
    entry = DreamEntry(
        title=data.get('title'),
        content=data.get('content'),
        dream_date=datetime.fromisoformat(data.get('dream_date')) if data.get('dream_date') else datetime.now(),
        tags=','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags'),
        sleep_quality=data.get('sleep_quality')
    )
    
    # Perform NLP analysis
    analysis = analyzer.analyze_dream(entry.content)
    
    # Store analysis results
    entry.sentiment_score = analysis['sentiment_score']
    entry.emotions = json.dumps(analysis['emotions'])
    entry.entities = json.dumps(analysis['entities'])
    entry.themes = json.dumps(analysis['themes'])
    entry.dream_intensity = analysis['dream_intensity']
    entry.stress_level = analysis['stress_level']
    
    # Save to database
    db.session.add(entry)
    db.session.commit()
    
    return jsonify(entry.to_dict()), 201


@app.route('/api/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update an existing dream entry"""
    entry = DreamEntry.query.get_or_404(entry_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'title' in data:
        entry.title = data['title']
    if 'content' in data:
        entry.content = data['content']
        # Re-analyze if content changed
        analysis = analyzer.analyze_dream(entry.content)
        entry.sentiment_score = analysis['sentiment_score']
        entry.emotions = json.dumps(analysis['emotions'])
        entry.entities = json.dumps(analysis['entities'])
        entry.themes = json.dumps(analysis['themes'])
        entry.dream_intensity = analysis['dream_intensity']
        entry.stress_level = analysis['stress_level']
    
    if 'dream_date' in data:
        entry.dream_date = datetime.fromisoformat(data['dream_date'])
    if 'tags' in data:
        entry.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
    if 'sleep_quality' in data:
        entry.sleep_quality = data['sleep_quality']
    
    entry.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(entry.to_dict())


@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a dream entry"""
    entry = DreamEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Entry deleted successfully'})


@app.route('/api/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get overview analytics for dashboard"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    entries = DreamEntry.query.filter(
        DreamEntry.dream_date >= start_date
    ).order_by(DreamEntry.dream_date).all()
    
    if not entries:
        return jsonify({
            'total_entries': 0,
            'avg_sentiment': 0,
            'dominant_emotion': 'none',
            'stress_trend': 'no data'
        })
    
    # Calculate statistics
    total_entries = len(entries)
    avg_sentiment = sum(e.sentiment_score for e in entries if e.sentiment_score) / total_entries
    
    # Emotion distribution
    emotion_totals = {}
    for entry in entries:
        if entry.emotions:
            emotions = json.loads(entry.emotions)
            for emotion, score in emotions.items():
                emotion_totals[emotion] = emotion_totals.get(emotion, 0) + score
    
    dominant_emotion = max(emotion_totals.items(), key=lambda x: x[1])[0] if emotion_totals else 'neutral'
    
    # Stress trend
    stress_levels = [e.stress_level for e in entries if e.stress_level is not None]
    if len(stress_levels) >= 2:
        first_half_avg = sum(stress_levels[:len(stress_levels)//2]) / (len(stress_levels)//2)
        second_half_avg = sum(stress_levels[len(stress_levels)//2:]) / (len(stress_levels) - len(stress_levels)//2)
        
        if second_half_avg > first_half_avg * 1.1:
            stress_trend = 'increasing'
        elif second_half_avg < first_half_avg * 0.9:
            stress_trend = 'decreasing'
        else:
            stress_trend = 'stable'
    else:
        stress_trend = 'insufficient data'
    
    return jsonify({
        'total_entries': total_entries,
        'avg_sentiment': round(avg_sentiment, 3),
        'dominant_emotion': dominant_emotion,
        'stress_trend': stress_trend,
        'date_range': {
            'start': start_date.isoformat(),
            'end': datetime.now().isoformat()
        }
    })


@app.route('/api/analytics/timeline', methods=['GET'])
def get_timeline_data():
    """Get timeline data for emotion trends"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    entries = DreamEntry.query.filter(
        DreamEntry.dream_date >= start_date
    ).order_by(DreamEntry.dream_date).all()
    
    timeline = []
    for entry in entries:
        emotions = json.loads(entry.emotions) if entry.emotions else {}
        timeline.append({
            'date': entry.dream_date.isoformat(),
            'sentiment': entry.sentiment_score,
            'emotions': emotions,
            'stress': entry.stress_level,
            'intensity': entry.dream_intensity
        })
    
    return jsonify(timeline)


@app.route('/api/analytics/themes', methods=['GET'])
def get_theme_analysis():
    """Get recurring themes analysis"""
    days = request.args.get('days', 90, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    entries = DreamEntry.query.filter(
        DreamEntry.dream_date >= start_date
    ).all()
    
    # Aggregate themes
    all_themes = []
    for entry in entries:
        if entry.themes:
            all_themes.extend(json.loads(entry.themes))
    
    # Count occurrences
    from collections import Counter
    theme_counts = Counter(all_themes)
    
    return jsonify({
        'themes': [
            {'name': theme, 'count': count}
            for theme, count in theme_counts.most_common(20)
        ]
    })


@app.route('/api/analytics/entities', methods=['GET'])
def get_entity_analysis():
    """Get recurring entities (people, places, symbols)"""
    days = request.args.get('days', 90, type=int)
    start_date = datetime.now() - timedelta(days=days)
    
    entries = DreamEntry.query.filter(
        DreamEntry.dream_date >= start_date
    ).all()
    
    # Aggregate entities by category
    all_entities = {
        'people': [],
        'places': [],
        'symbols': []
    }
    
    for entry in entries:
        if entry.entities:
            entities = json.loads(entry.entities)
            all_entities['people'].extend(entities.get('people', []))
            all_entities['places'].extend(entities.get('places', []))
            all_entities['symbols'].extend(entities.get('symbols', []))
    
    # Count occurrences
    from collections import Counter
    
    return jsonify({
        'people': [
            {'name': name, 'count': count}
            for name, count in Counter(all_entities['people']).most_common(10)
        ],
        'places': [
            {'name': name, 'count': count}
            for name, count in Counter(all_entities['places']).most_common(10)
        ],
        'symbols': [
            {'name': name, 'count': count}
            for name, count in Counter(all_entities['symbols']).most_common(15)
        ]
    })


@app.route('/api/summaries/generate', methods=['POST'])
def generate_summary():
    """Generate a period summary (weekly or monthly)"""
    data = request.get_json()
    period_type = data.get('period_type', 'weekly')
    
    # Calculate period dates
    end_date = datetime.now()
    if period_type == 'weekly':
        start_date = end_date - timedelta(days=7)
    else:  # monthly
        start_date = end_date - timedelta(days=30)
    
    # Get entries for the period
    entries = DreamEntry.query.filter(
        DreamEntry.dream_date >= start_date,
        DreamEntry.dream_date <= end_date
    ).all()
    
    if not entries:
        return jsonify({'error': 'No entries found for this period'}), 404
    
    # Generate insights
    insights = analyzer.generate_insights(entries)
    
    # Create summary
    summary = EmotionSummary(
        period_type=period_type,
        period_start=start_date,
        period_end=end_date,
        total_entries=insights['total_entries'],
        avg_sentiment=insights['avg_sentiment'],
        dominant_emotion=insights['dominant_emotion'],
        emotion_distribution=json.dumps(insights['emotion_distribution']),
        recurring_themes=json.dumps(insights['recurring_themes']),
        stress_trend=insights['stress_trend'],
        summary_text=f"During this {period_type} period, you recorded {insights['total_entries']} dreams. "
                     f"Your dominant emotion was {insights['dominant_emotion']} with an average sentiment of "
                     f"{insights['avg_sentiment']:.2f}. Stress levels are {insights['stress_trend']}.",
        recommendations=_generate_recommendations(insights)
    )
    
    db.session.add(summary)
    db.session.commit()
    
    return jsonify(summary.to_dict()), 201


@app.route('/api/summaries', methods=['GET'])
def get_summaries():
    """Get all generated summaries"""
    summaries = EmotionSummary.query.order_by(
        EmotionSummary.period_start.desc()
    ).all()
    
    return jsonify([summary.to_dict() for summary in summaries])


@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Export dream entries as PDF"""
    if not Config.ENABLE_EXPORT:
        return jsonify({'error': 'Export feature is disabled'}), 403
    
    data = request.get_json()
    entry_ids = data.get('entry_ids', [])
    
    if not entry_ids:
        # Export all entries
        entries = DreamEntry.query.order_by(DreamEntry.dream_date.desc()).all()
    else:
        entries = DreamEntry.query.filter(DreamEntry.id.in_(entry_ids)).all()
    
    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    y_position = height - 50
    
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, y_position, "Dream Journal Export")
    y_position -= 40
    
    p.setFont("Helvetica", 10)
    p.drawString(50, y_position, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y_position -= 30
    
    for entry in entries:
        # Check if we need a new page
        if y_position < 100:
            p.showPage()
            y_position = height - 50
        
        # Entry title
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_position, entry.title or "Untitled Dream")
        y_position -= 20
        
        # Date and sentiment
        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"Date: {entry.dream_date.strftime('%Y-%m-%d')}")
        p.drawString(300, y_position, f"Sentiment: {entry.sentiment_score:.2f}")
        y_position -= 20
        
        # Content (truncate if too long)
        p.setFont("Helvetica", 9)
        content_lines = entry.content[:500].split('\n')
        for line in content_lines[:10]:  # Max 10 lines per entry
            if y_position < 50:
                p.showPage()
                y_position = height - 50
            p.drawString(50, y_position, line[:100])
            y_position -= 15
        
        y_position -= 20
    
    p.save()
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'dream_journal_{datetime.now().strftime("%Y%m%d")}.pdf'
    )


@app.route('/api/tags', methods=['GET'])
def get_all_tags():
    """Get all unique tags used"""
    entries = DreamEntry.query.all()
    all_tags = set()
    
    for entry in entries:
        if entry.tags:
            all_tags.update(tag.strip() for tag in entry.tags.split(','))
    
    return jsonify(sorted(list(all_tags)))


def _generate_recommendations(insights):
    """Generate personalized recommendations based on insights"""
    recommendations = []
    
    # Sentiment-based recommendations
    if insights['avg_sentiment'] < -0.3:
        recommendations.append("Your dreams show negative sentiment. Consider stress-reduction practices before bed.")
    elif insights['avg_sentiment'] > 0.3:
        recommendations.append("Your dreams are predominantly positive. Keep up your good sleep hygiene!")
    
    # Stress-based recommendations
    if insights['stress_trend'] == 'increasing':
        recommendations.append("Stress levels in your dreams are increasing. Try meditation or relaxation exercises.")
    
    # Emotion-based recommendations
    if insights['dominant_emotion'] == 'fear':
        recommendations.append("Fear is prominent in your dreams. Consider journaling before bed to process anxieties.")
    elif insights['dominant_emotion'] == 'sadness':
        recommendations.append("Notice sadness themes. Reach out to friends or consider speaking with a counselor.")
    
    if not recommendations:
        recommendations.append("Your dream patterns look balanced. Continue regular journaling for best insights.")
    
    return ' '.join(recommendations)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
