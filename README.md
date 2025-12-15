# Dream Journal - Emotion Tracker 🌙

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20VADER-orange.svg)

A comprehensive **Dream Journal Emotion Tracker** application that helps users understand their subconscious emotional patterns through advanced NLP analysis, beautiful visualizations, and personalized insights.

![Dream Journal Dashboard](https://img.shields.io/badge/Status-Ready%20to%20Use-success)

## 📸 Screenshots

> *Note: Add screenshots of your running application here*

## 🌟 Why Dream Journal?

- **🔒 100% Private** - All data stays on your device
- **🧠 AI-Powered** - Advanced NLP analyzes your dreams
- **📊 Beautiful Insights** - Interactive charts show patterns
- **🎯 Actionable** - Get personalized recommendations
- **🆓 Free & Open Source** - MIT licensed

## ✨ Features

### 📝 Dream Entry Management
- **Flexible Input**: Record dreams with structured forms or free text
- **Rich Metadata**: Add titles, tags, dream dates, and sleep quality ratings
- **Search & Filter**: Easily find past dreams by keywords or tags
- **Edit & Delete**: Full CRUD operations on all entries

### 🧠 Advanced NLP Analysis
- **Sentiment Analysis**: VADER + TextBlob dual sentiment scoring
- **Emotion Detection**: Track 8 core emotions (joy, sadness, fear, anger, surprise, disgust, trust, anticipation)
- **Entity Extraction**: Identify people, places, and symbols in dreams using spaCy
- **Theme Recognition**: Detect common dream themes (flying, falling, chase, water, etc.)
- **Stress Indicators**: Measure stress levels through keyword analysis
- **Dream Intensity**: Calculate overall dream intensity metrics

### 📊 Interactive Visualizations
- **Emotion Timeline**: Track emotional trends over time
- **Emotion Distribution**: Pie chart showing emotion breakdown
- **Calendar Heatmap**: Visual dream frequency and intensity calendar
- **Stress Trend Charts**: Monitor stress patterns with moving averages
- **Theme Analysis**: Bar charts of recurring dream themes
- **Sentiment Gauges**: Real-time sentiment indicators

### 🔮 Insights & Predictions
- **Weekly/Monthly Summaries**: Auto-generated period reports
- **Trend Analysis**: Identify increasing/decreasing stress patterns
- **Pattern Detection**: Discover cyclical themes and correlations
- **Mood Predictions**: Linear regression-based sentiment forecasting
- **Personalized Recommendations**: AI-generated wellness suggestions
- **Sleep Quality Correlation**: Analyze sleep quality impact on dreams

### 🎨 User Experience
- **Modern UI**: Clean, responsive Bootstrap design
- **Dark Theme Ready**: Eye-friendly color scheme
- **Mobile Responsive**: Works on all device sizes
- **Privacy First**: Local SQLite database, all processing on-device
- **Export Options**: PDF export for backups and sharing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```powershell
cd "c:\Users\ayush\OneDrive\Desktop\Development\1512"
```

2. **Create a virtual environment** (recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Download spaCy language model**
```powershell
python -m spacy download en_core_web_sm
```

5. **Initialize the database**
```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### Running the Application

```powershell
python app.py
```

The application will start on **http://localhost:5000**

Open your browser and navigate to the address to start using the Dream Journal!

## 📖 Usage Guide

### Recording a Dream

1. Click **"+ New Entry"** button in the navigation bar
2. Fill in the details:
   - **Title** (optional): Give your dream a memorable name
   - **Dream Date**: When did you have this dream?
   - **Content**: Describe your dream in detail (the more, the better!)
   - **Tags**: Add relevant keywords (comma-separated)
   - **Sleep Quality**: Rate 1-10 using the slider
3. Click **"Save & Analyze"**
4. The app automatically analyzes your dream using NLP

### Viewing Your Dashboard

The **Dashboard** tab shows:
- Total entries and average sentiment
- Dominant emotion across all dreams
- Current stress trend
- Interactive charts showing patterns over time
- Calendar heatmap of dream activity

### Exploring Entries

The **Entries** tab allows you to:
- Browse all recorded dreams
- Search by content or title
- Filter by tags
- Click any dream card to view full analysis
- Edit or delete entries

### Generating Insights

The **Insights** tab provides:
- **Weekly Summary**: Generate analysis of the past 7 days
- **Monthly Summary**: Generate analysis of the past 30 days
- **PDF Export**: Download all entries as a formatted PDF
- **Past Summaries**: View previously generated reports

## 🏗️ Project Structure

```
1512/
├── app.py                  # Main Flask application & API routes
├── config.py              # Configuration settings
├── models.py              # SQLAlchemy database models
├── nlp_analyzer.py        # NLP analysis engine
├── predictor.py           # Prediction & pattern detection
├── visualizations.py      # Plotly chart generation
├── requirements.txt       # Python dependencies
├── dream_journal.db       # SQLite database (created on first run)
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── css/
    │   └── style.css      # Custom styling
    └── js/
        └── app.js         # Frontend JavaScript
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Database**: Change from SQLite to PostgreSQL/MySQL
- **Emotion Categories**: Add or modify tracked emotions
- **Color Scheme**: Customize visualization colors
- **Privacy Settings**: Enable/disable features
- **Reminder Settings**: Set notification preferences

## 🧪 Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database management
- **spaCy**: Named entity recognition
- **VADER**: Sentiment analysis
- **TextBlob**: Additional NLP processing
- **scikit-learn**: Machine learning for predictions

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Plotly.js**: Interactive visualizations
- **Font Awesome**: Icons
- **Vanilla JavaScript**: No heavy frameworks, fast & lightweight

### Analysis
- **Sentiment Analysis**: Dual scoring (VADER + TextBlob)
- **Emotion Detection**: Keyword-based multi-emotion tracking
- **Entity Extraction**: spaCy NER pipeline
- **Theme Recognition**: Pattern matching algorithms
- **Trend Prediction**: Linear regression models

## 📊 API Endpoints

The application provides a RESTful API:

### Entries
- `GET /api/entries` - List all entries (paginated)
- `POST /api/entries` - Create new entry with analysis
- `GET /api/entries/<id>` - Get specific entry
- `PUT /api/entries/<id>` - Update entry
- `DELETE /api/entries/<id>` - Delete entry

### Analytics
- `GET /api/analytics/overview` - Dashboard statistics
- `GET /api/analytics/timeline` - Emotion timeline data
- `GET /api/analytics/themes` - Theme frequency analysis
- `GET /api/analytics/entities` - Entity occurrence data

### Summaries
- `POST /api/summaries/generate` - Generate period summary
- `GET /api/summaries` - List all summaries

### Utility
- `GET /api/tags` - Get all unique tags
- `POST /api/export/pdf` - Export entries as PDF

## 🎯 Key Features Explained

### Sentiment Scoring
- **Range**: -1 (very negative) to +1 (very positive)
- **Method**: Combines VADER and TextBlob for accuracy
- **Use**: Quick overview of dream emotional tone

### Emotion Detection
- **Categories**: 8 emotions based on Plutchik's wheel
- **Method**: Keyword matching with normalization
- **Output**: Score 0-1 for each emotion category

### Stress Detection
- **Indicators**: Chasing, falling, being late, losing teeth, etc.
- **Range**: 0 (no stress) to 1 (high stress)
- **Use**: Track anxiety patterns over time

### Dream Intensity
- **Factors**: Word count, punctuation, emotional content
- **Range**: 0 (calm) to 1 (intense)
- **Use**: Identify vivid vs. vague dreams

## 🔒 Privacy & Security

- **Local Processing**: All NLP happens on your machine
- **Local Storage**: SQLite database stored locally
- **No Cloud**: No data sent to external servers
- **Export Control**: You own and control your data
- **Secure**: No user authentication needed (single-user app)

## 🛠️ Troubleshooting

### spaCy model not found
```powershell
python -m spacy download en_core_web_sm
```

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Database errors
Delete `dream_journal.db` and reinitialize:
```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 🚧 Future Enhancements

Potential features for expansion:
- 🌐 Multi-user support with authentication
- 📱 Mobile app (React Native/Flutter)
- 🔊 Voice-to-text dream recording
- 🌍 Dream symbol dictionary/interpretation
- 👥 Community features (anonymous sharing)
- 📧 Email reminders for journaling
- 🧬 Advanced ML models (BERT, GPT fine-tuning)
- 📈 Correlation with external factors (weather, moon phases)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Ways to Contribute:
- 🐛 Report bugs
- ✨ Suggest new features
- 🔧 Submit pull requests
- 📝 Improve documentation
- ⭐ Star this repository

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 💡 Tips for Best Results

1. **Be Detailed**: More text = better analysis
2. **Record Immediately**: Capture dreams right when you wake
3. **Be Consistent**: Regular journaling improves insights
4. **Use Tags**: Makes finding patterns easier
5. **Track Sleep Quality**: Helps identify correlations
6. **Review Summaries**: Weekly reviews reveal trends

## 📧 Support

For issues or questions:
- 📖 Check the [troubleshooting section](#-troubleshooting)
- 💬 Open an [issue](../../issues)
- 📧 Review existing discussions

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

## 🙏 Acknowledgments

This project uses amazing open-source libraries:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [spaCy](https://spacy.io/) - Industrial-strength NLP
- [VADER](https://github.com/cjhutto/vaderSentiment) - Sentiment analysis
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [TextBlob](https://textblob.readthedocs.io/) - Text processing

## 🌟 Acknowledgments

Built with:
- Flask framework
- spaCy NLP library
- VADER sentiment analysis
- Plotly visualization
- Bootstrap UI components

---

**Sweet dreams and happy journaling! 🌙✨**
