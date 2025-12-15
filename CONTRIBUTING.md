# Contributing to Dream Journal

Thank you for your interest in contributing to the Dream Journal Emotion Tracker! 🌙

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in Issues
- Create a new issue with a clear description
- Include steps to reproduce the bug
- Mention your Python version and OS

### Suggesting Enhancements
- Open an issue with the "enhancement" label
- Clearly describe the feature and its benefits
- Provide examples if possible

### Pull Requests
1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dream-journal.git
cd dream-journal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Run the app
python app.py
```

## Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Keep functions focused and modular
- Comment complex logic

## Testing
- Test all new features thoroughly
- Ensure existing functionality still works
- Test on different browsers if changing frontend

## Areas for Contribution
- 🐛 Bug fixes
- ✨ New NLP models or analysis techniques
- 📊 Additional visualizations
- 🎨 UI/UX improvements
- 📱 Mobile responsiveness
- 🌍 Internationalization
- 📝 Documentation improvements
- ♿ Accessibility enhancements

## Questions?
Feel free to open an issue for any questions!

Thank you for contributing! 💙
