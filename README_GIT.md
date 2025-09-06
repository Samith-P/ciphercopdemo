# SMS & Email Notification System

A Flask-based web application for sending email and SMS notifications with OTP verification. This system supports multiple email providers (Gmail SMTP, Mailtrap) and SMS via Twilio Verify API.

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd sms-email-notification
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` with your actual credentials (see setup guides below).

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 📋 Features

- ✅ **Email Notifications** with HTML templates
- ✅ **SMS OTP** via Twilio Verify API
- ✅ **Email OTP** with Redis caching
- ✅ **Multiple Email Providers** (Gmail, Mailtrap)
- ✅ **Modern Web Interface** with Bootstrap 5
- ✅ **Real-time Validation** and notifications
- ✅ **Configuration Testing** tools

## 🔧 Setup Guides

### Gmail Setup
See [GMAIL_SETUP.md](GMAIL_SETUP.md) for detailed instructions.

### Twilio Setup
1. Create account at [twilio.com](https://www.twilio.com/)
2. Get Account SID and Auth Token
3. Create a Verify Service and get Service SID
4. Add credentials to `.env` file

### Redis Setup (Optional)
- Install Redis locally or use cloud service
- Default: `redis://localhost:6379/0`

## 📁 Project Structure

```
sms-email-notification/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── GMAIL_SETUP.md            # Gmail configuration guide
├── EMAIL_SMS_IMPLEMENTATION_GUIDE.md  # Detailed implementation guide
├── setup.bat                  # Windows setup script
├── setup.sh                   # Linux/Mac setup script
├── templates/
│   └── index.html            # Web interface
└── static/
    ├── css/
    │   └── style.css         # Custom styles
    └── js/
        └── script.js         # Frontend JavaScript
```

## 🔐 Security Notes

- ⚠️ **Never commit `.env` files** - they contain sensitive credentials
- ✅ Use app passwords for Gmail (not regular passwords)
- ✅ Rotate API keys regularly
- ✅ Use HTTPS in production

## 🛠️ Development

### Local Development
```bash
# Clone and setup
git clone <repo-url>
cd sms-email-notification
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your credentials
python app.py
```

### Testing
- Use Mailtrap for email testing (emails won't be delivered)
- Use Twilio's free tier for SMS testing
- Check `/config` endpoint for service status

## 📚 Documentation

- [EMAIL_SMS_IMPLEMENTATION_GUIDE.md](EMAIL_SMS_IMPLEMENTATION_GUIDE.md) - Complete implementation guide
- [GMAIL_SETUP.md](GMAIL_SETUP.md) - Gmail SMTP setup instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter issues:
1. Check the setup guides
2. Verify environment variables
3. Test service connections using built-in tools
4. Check the browser console for errors

---

**🎉 Happy coding!** If you find this project useful, please give it a ⭐ on GitHub.
