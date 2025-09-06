# 📧📱 Simple Email & SMS Notification System

A simple Flask-based web application for sending email and SMS notifications with OTP verification.

## 🚀 Features

- **Email Notifications**
  - Send simple emails with custom subject and message
  - Email OTP verification with HTML templates
  - Gmail SMTP integration
  - Real-time email validation

- **SMS Notifications**
  - SMS OTP verification via Twilio Verify API
  - International phone number support
  - Automatic phone number formatting
  - Real-time SMS delivery status

- **User Interface**
  - Modern, responsive Bootstrap 5 design
  - Real-time activity logs
  - Configuration status monitoring
  - Interactive forms with validation
  - Sweet Alert notifications

- **Backend Features**
  - Redis caching for OTP storage (with fallback)
  - Error handling and logging
  - RESTful API endpoints
  - Configuration validation

## 📋 Prerequisites

- Python 3.7+
- Gmail account with App Password
- Twilio account (for SMS)
- Redis server (optional, has fallback)

## 🛠️ Installation

1. **Clone or create the project directory:**
   ```bash
   cd simple_notification_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   # Gmail Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_VERIFY_SERVICE_SID=your_service_sid
   
   # Redis (Optional)
   REDIS_URL=redis://localhost:6379/0
   ```

## 🔧 Configuration Guide

### Gmail Setup:

1. **Enable 2-Factor Authentication** in your Google account
2. **Generate App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `EMAIL_PASSWORD`

### Twilio Setup:

1. **Create Twilio Account:** https://www.twilio.com/
2. **Get credentials:**
   - Account SID and Auth Token from Dashboard
3. **Create Verify Service:**
   - Go to Verify → Services
   - Create new service
   - Copy Service SID

### Redis Setup (Optional):

```bash
# Install Redis (Windows)
# Download from: https://redis.io/download

# Install Redis (Ubuntu/Debian)
sudo apt update
sudo apt install redis-server

# Start Redis
redis-server

# Test Redis
redis-cli ping
```

## 🚀 Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   ```
   http://localhost:5000
   ```

## 📱 Usage

### Email Notifications:

1. **Simple Email:**
   - Enter recipient email
   - Add subject and message
   - Click "Send Email"

2. **Email OTP:**
   - Enter email address
   - Click "Send OTP"
   - Check email for OTP
   - Enter OTP and verify

### SMS Notifications:

1. **SMS OTP:**
   - Enter 10-digit phone number
   - Click "Send OTP"
   - Check SMS for OTP
   - Enter OTP and verify

## 🔌 API Endpoints

### Email Endpoints:
- `POST /send_email` - Send simple email
- `POST /send_email_otp` - Send email OTP
- `POST /verify_email_otp` - Verify email OTP

### SMS Endpoints:
- `POST /send_sms` - Send SMS OTP
- `POST /verify_sms` - Verify SMS OTP

### Utility:
- `GET /config` - Check configuration status

## 📁 Project Structure

```
simple_notification_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── script.js     # JavaScript functionality
```

## 🧪 Testing

### Test Email:
```bash
curl -X POST http://localhost:5000/send_email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","subject":"Test","message":"Hello World"}'
```

### Test SMS:
```bash
curl -X POST http://localhost:5000/send_sms \
  -H "Content-Type: application/json" \
  -d '{"phone":"1234567890"}'
```

## 🔍 Troubleshooting

### Email Issues:
- **Authentication Error:** Use App Password, not regular password
- **SMTP Error:** Check Gmail settings and 2FA
- **Connection Error:** Verify EMAIL_HOST and EMAIL_PORT

### SMS Issues:
- **Twilio Error:** Verify Account SID and Auth Token
- **Service Error:** Check Verify Service SID
- **Phone Format:** Use 10-digit number without country code

### Redis Issues:
- **Connection Error:** Application will use fallback storage
- **Redis Not Found:** Install Redis or disable in code

## 🎯 Features Included from Original Repo

This implementation includes all major features from the original AIORI services repo:

✅ **Email System:**
- Multiple email types support
- HTML email templates
- OTP generation and verification
- SMTP configuration
- Error handling

✅ **SMS System:**
- Twilio Verify API integration
- International phone support
- OTP verification
- Real-time status updates

✅ **Frontend:**
- Modern responsive design
- Real-time validation
- Activity logging
- Configuration monitoring
- Interactive UI elements

✅ **Backend:**
- Flask REST API
- Redis caching with fallback
- Environment configuration
- Error handling and logging

## 🚀 Next Steps

1. **Production Deployment:**
   - Use production WSGI server (Gunicorn)
   - Configure reverse proxy (Nginx)
   - Set up SSL certificates
   - Use production Redis instance

2. **Enhanced Features:**
   - User authentication
   - Rate limiting
   - Email templates editor
   - SMS templates
   - Analytics dashboard

3. **Scaling:**
   - Database integration
   - Queue system (Celery)
   - Load balancing
   - Monitoring and logging

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Verify all environment variables
3. Check service configurations
4. Review activity logs in the web interface

---

**🎉 Your simple notification system is ready!** Open http://localhost:5000 and start sending notifications!
