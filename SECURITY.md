# Security Policy

## Supported Versions

Currently supported versions of Dream Journal:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within Dream Journal, please follow these steps:

1. **Do Not** open a public issue
2. Email the details to the repository maintainer (check GitHub profile)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- Acknowledgment of your report within 48 hours
- Regular updates on the progress
- Credit in the changelog (if desired)

## Security Considerations

### Data Privacy
- All dream data is stored locally in SQLite
- No data is sent to external servers
- All NLP processing happens on-device

### Best Practices
- Keep your Python dependencies updated
- Use the application on a secure, personal device
- Regular backups of your `dream_journal.db` file
- Don't expose the Flask development server to the internet

### Production Deployment
If deploying for production use:
- Use a production WSGI server (Gunicorn, uWSGI)
- Enable HTTPS
- Set strong SECRET_KEY in environment variables
- Use proper authentication if multi-user
- Regular security updates for dependencies

## Secure Usage Tips

1. **Backup Your Data**: Export PDFs regularly
2. **Keep Private**: Don't share your database file
3. **Update Dependencies**: Run `pip install --upgrade -r requirements.txt` periodically
4. **Local Only**: Don't expose port 5000 to the internet in production

Thank you for helping keep Dream Journal secure! 🔒
