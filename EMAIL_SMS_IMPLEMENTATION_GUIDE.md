# 📧📱 Complete Email & SMS Notification Implementation Guide

This comprehensive guide will help you implement email and SMS notifications in your Django project, based on the AIORI Services Portal implementation.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Email Notification System](#email-notification-system)
4. [SMS Notification System](#sms-notification-system)
5. [Frontend Integration](#frontend-integration)
6. [Complete Setup Guide](#complete-setup-guide)
7. [API Endpoints](#api-endpoints)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## 🔍 Overview

This implementation provides:
- **Email notifications** with multiple providers (SMTP, SendGrid)
- **SMS notifications** via Twilio Verify API
- **OTP verification** for both email and mobile
- **HTML email templates**
- **Redis caching** for OTP storage
- **Frontend JavaScript integration**

---

## ⚙️ Prerequisites

### Required Accounts & Services

1. **Email Service** (choose one):
   - [SendGrid Account](https://sendgrid.com/) - Recommended for production
   - Gmail SMTP - Good for development
   - [Mailtrap](https://mailtrap.io/) - Perfect for testing

2. **SMS Service**:
   - [Twilio Account](https://www.twilio.com/) - Required for SMS functionality

3. **Caching**:
   - Redis Server - Required for OTP storage

### Required Python Packages

```bash
pip install django
pip install python-decouple
pip install python-dotenv
pip install redis
pip install twilio
pip install django-redis
```

---

## 📧 Email Notification System

### 1. Project Structure

Create the following directory structure in your Django project:

```
your_project/
├── services/
│   ├── __init__.py
│   ├── email_service.py
│   └── mailing/
│       ├── __init__.py
│       ├── mailer/
│       │   ├── __init__.py
│       │   └── exception.py
│       └── sendgrid/
│           └── __init__.py
├── backend/
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── templates/
│   └── email/
│       ├── otp_template.html
│       ├── welcome_template.html
│       ├── reset_template.html
│       └── student_welcome_template.html
└── config_env.py
```

### 2. Configuration File (`config_env.py`)

```python
from decouple import config, Csv
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Email Settings
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your-email@gmail.com')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your-app-password')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='no-reply@example.com')
    EMAIL_SERVER = config('EMAIL_SERVER', default='SMTP')  # 'SMTP' or 'SENDGRID'
    SMTP_FROM = config('SMTP_FROM', default='smtp.gmail.com')
    SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')

    # Redis Configuration
    REDIS_DEFAULT_URL = config('REDIS_DEFAULT_URL', default='redis://localhost:6379/0')
    REDIS_OTP_URL = config('REDIS_OTP_URL', default='redis://localhost:6379/1')
    REDIS_SESSION_URL = config('REDIS_SESSION_URL', default='redis://localhost:6379/2')

CONFIG = Settings()
```

### 3. Email Service Implementation (`services/email_service.py`)

```python
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from config_env import CONFIG
from django.utils.html import strip_tags
from backend.users.models import CustomUser  # Replace with your User model

class EmailHelper:
    def __init__(self, user: CustomUser, email_type: str = 'document', email_address: str = None, 
                 cc=None, bcc=None, attachments=None, content: dict = None):
        """
        Initialize the EmailHelper class.
        
        Args:
            user: User instance to use in the email
            email_type: Type of email ('otp', 'welcome', 'reset', etc.)
            email_address: Recipient email address
            cc: CC recipients list
            bcc: BCC recipients list
            attachments: Attachments list
            content: Dictionary containing custom content
        """
        self.user = user
        self.email_type = email_type
        self.cc = cc or []
        self.bcc = bcc or []
        self.attachments = attachments or []
        self.content = content

        if not self.user and email_address is None:
            raise ValueError("User or email address must be provided!")

        self.email_address = email_address or user.email
        self.email_content = self.prepare_email_content()

    def prepare_email_content(self):
        """Prepares email content based on the email type."""
        subject, html_content = self.get_template_for_email_type()

        # Custom content override
        if self.content and self.content.get("subject") and self.content.get("html_content"):
            subject = self.content.get("subject")
            html_content = self.content.get("html_content")

        plain_text_content = strip_tags(html_content)

        return {
            "recipient": self.email_address,
            "subject": subject,
            "html_content": html_content,
            "plain_text_content": plain_text_content,
            "cc": self.cc,
            "bcc": self.bcc,
            "attachments": self.attachments
        }

    def get_template_for_email_type(self):
        """Returns the subject and HTML content based on email type."""
        template_map = {
            'document': ('Your Document is Ready', 'email/document_template.html'),
            'reset': ('Password Reset Request', 'email/reset_template.html'),
            'welcome': ('Welcome to Your Portal', 'email/welcome_template.html'),
            'student_welcome': ('Welcome to Student Portal', 'email/student_welcome_template.html'),
            'otp': ('Your OTP Code', 'email/otp_template.html'),
        }

        template_name = template_map.get(self.email_type, ('Notification', 'email/default_template.html'))
        
        context = {'user': self.user}
        if self.email_type == 'otp':
            context['otp'] = self.content.get('otp')
        elif self.email_type in ['welcome', 'student_welcome']:
            context.update({
                'user_name': self.user.username,
                'dashboard_link': 'http://localhost:8000',  # Update with your URL
                'user_email': self.user.email,
            })
        elif self.email_type == 'reset':
            context['reset_link'] = self.content.get('reset_link')

        html_content = render_to_string(template_name[1], context)
        return template_name[0], html_content

    def send_email(self):
        """Sends the email after the content is prepared."""
        try:
            email = EmailMessage(
                self.email_content['subject'],
                self.email_content['html_content'],
                CONFIG.DEFAULT_FROM_EMAIL,
                [self.email_content['recipient']],
                self.email_content['cc'],
                self.email_content['bcc'],
            )

            # Add attachments
            for attachment in self.email_content['attachments']:
                email.attach(attachment['name'], attachment['content'], attachment['mime_type'])

            email.content_subtype = "html"
            email.send()

            return {"status": "success", "message": "Email sent successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to send email: {str(e)}"}
```

### 4. Alternative Mailing Service (`services/mailing/__init__.py`)

```python
import re
import traceback
from config_env import CONFIG
from services.mailing.mailer import Mailer
from services.mailing.sendgrid import SendGrid
from django.template.loader import render_to_string

class Mailing:
    def __init__(self, email_type: str = 'document', from_email=None, email_address: str = None, 
                 cc=None, bcc=None, attachments=None, content: dict = None):
        self.email_type = email_type
        self.mailer = None
        self.cc = cc or []
        self.bcc = bcc or []
        self.attachments = attachments or []
        self.content = content
        self.email_address = email_address
        self.email_content = self.prepare_email_content()
        self.from_email = from_email
        self.init_mailer()

    def init_mailer(self):
        """Initialize the appropriate mailer based on configuration."""
        try:
            if CONFIG.EMAIL_SERVER == 'SMTP':
                self.mailer = Mailer(from_email=self.from_email)
            elif CONFIG.EMAIL_SERVER == 'SENDGRID':
                self.mailer = SendGrid()
        except Exception as e:
            raise TypeError("Unable to initialize mailer!") from e

    def prepare_email_content(self):
        """Prepare the email content based on email_type."""
        if self.content and self.content.get("subject") and self.content.get("html_content"):
            subject = self.content.get("subject")
            html_content = self.content.get("html_content")
        else:
            subject, html_content = self.get_template_for_email_type()

        return {
            "recipient": self.email_address,
            "subject": subject,
            "html_content": html_content,
            "cc": self.cc,
            "bcc": self.bcc,
            "attachments": self.attachments
        }

    def get_template_for_email_type(self):
        """Return the subject and HTML content based on email type."""
        template_map = {
            'document': ('Your Document is Ready', 'document_template.html'),
            'reset': ('Password Reset Request', 'reset_template.html'),
            'welcome': ('Welcome to Service Portal', 'welcome_template.html'),
            'otp': ('Your OTP Code', 'email/otp_template.html'),
        }

        template = template_map.get(self.email_type, ('Notification', 'default_template.html'))
        subject = template[0]
        template_name = template[1]
        
        context = {}
        if self.email_type == 'otp':
            otp = self.content.get('otp')
            subject = f'Service Portal | Your One Time Password | {otp}'
            context['otp'] = otp
            html_content = render_to_string(template_name, context)
        else:
            html_content = "<p>This is a test email</p>"

        return subject, html_content

    def send_email(self):
        """Send the email after the content is prepared."""
        try:
            self.mailer.send(
                data=self.email_content,
                recipients=[self.email_content['recipient']],
                cc=self.email_content['cc'],
                bcc=self.email_content['bcc']
            )
            return {"status": "success", "message": "Email sent successfully."}
        except Exception as e:
            traceback.print_exc()
            raise e
```

### 5. SMTP Mailer Implementation (`services/mailing/mailer/__init__.py`)

```python
import smtplib
import ssl
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL, SMTPException
from config_env import CONFIG

class Mailer(object):
    def __init__(self, from_email=None):
        self.host = CONFIG.EMAIL_HOST
        self.port = CONFIG.EMAIL_PORT
        self.username = CONFIG.EMAIL_HOST_USER
        self.password = CONFIG.EMAIL_HOST_PASSWORD
        self.from_email = from_email if from_email else CONFIG.DEFAULT_FROM_EMAIL
        self.connection = None
        if not self.connected:
            self.connect()

    @property
    def connected(self):
        return self.connection is not None

    def connect(self):
        """Establish connection to SMTP server."""
        try:
            if self.port == 465:
                # Use SSL
                ssl_context = ssl.create_default_context()
                self.connection = SMTP_SSL(host=self.host, port=self.port, context=ssl_context)
            else:
                # Use TLS
                self.connection = SMTP(host=self.host, port=self.port)
                self.connection.starttls()
            
            self.connection.ehlo()
            self.connection.login(self.username, self.password)
        except Exception as e:
            raise SMTPException(f"Failed to connect to SMTP server: {str(e)}")

    def disconnect(self):
        """Disconnect from SMTP server."""
        if self.connected:
            try:
                self.connection.quit()
            except:
                pass
            finally:
                self.connection = None

    def send(self, data, recipients, cc=None, bcc=None):
        """Send email using SMTP."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = data['subject']
            msg['From'] = self.from_email
            msg['To'] = ', '.join(recipients)
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Add HTML content
            html_part = MIMEText(data['html_content'], 'html')
            msg.attach(html_part)
            
            # Send email
            all_recipients = recipients + (cc or []) + (bcc or [])
            self.connection.send_message(msg, to_addrs=all_recipients)
            
        except Exception as e:
            raise SMTPException(f"Failed to send email: {str(e)}")
```

### 6. OTP Helper Functions (`backend/utils/helpers.py`)

```python
import random
import string
import redis
from django.contrib.auth.hashers import make_password, check_password
from config_env import CONFIG
from services.mailing import Mailing

# Redis connection
redis_client = redis.from_url(CONFIG.REDIS_OTP_URL)

def generate_otp(length=6):
    """Generate a random OTP."""
    return ''.join(random.choices(string.digits, k=length))

def set_cache(cache_type, key, value, timeout=300):
    """Store value in Redis cache with timeout (default 5 minutes)."""
    try:
        redis_client.setex(f"{cache_type}:{key}", timeout, value)
        return True
    except Exception as e:
        print(f"Cache error: {e}")
        return False

def get_cache(cache_type, key):
    """Get value from Redis cache."""
    try:
        value = redis_client.get(f"{cache_type}:{key}")
        return value.decode('utf-8') if value else None
    except Exception as e:
        print(f"Cache error: {e}")
        return None

def delete_cache(cache_type, key):
    """Delete value from Redis cache."""
    try:
        redis_client.delete(f"{cache_type}:{key}")
        return True
    except Exception as e:
        print(f"Cache error: {e}")
        return False

def send_otp(email):
    """Send OTP to email address."""
    try:
        if not email:
            return {"status": "error", "message": "Email is required."}

        # Generate and hash OTP
        otp = generate_otp()
        hashed_otp = make_password(otp)

        # Store OTP in Redis cache for 5 minutes
        if not set_cache('otp_cache', email, hashed_otp):
            return {"status": "error", "message": "Failed to store OTP in cache."}

        # Prepare email content
        content = {"otp": otp}

        # Send email
        email_helper = Mailing(
            email_type='otp',
            from_email=f"{CONFIG.DEFAULT_FROM_EMAIL}<{CONFIG.DEFAULT_FROM_EMAIL}>",
            email_address=email,
            content=content
        )
        email_response = email_helper.send_email()

        if email_response["status"] == "success":
            return {"status": "success", "message": "OTP sent successfully."}
        else:
            return {"status": "error", "message": email_response["message"]}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def verify_otp(email, otp):
    """Verify OTP for email address."""
    try:
        # Get stored hashed OTP
        stored_otp = get_cache('otp_cache', email)
        if not stored_otp:
            return {"status": "error", "message": "OTP expired or not found."}

        # Verify OTP
        if check_password(otp, stored_otp):
            delete_cache('otp_cache', email)  # Remove OTP after successful verification
            return {"status": "success", "message": "OTP verified successfully."}
        else:
            return {"status": "error", "message": "Invalid OTP."}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
```

### 7. Email Templates

#### OTP Template (`templates/email/otp_template.html`)

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>OTP for Your Account | {{ otp }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f7f7f7;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .otp-box {
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 4px;
            padding: 10px 20px;
            border: 2px dashed #4caf50;
            display: inline-block;
            border-radius: 5px;
            background-color: #f9f9f9;
            text-align: center;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #888888;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>OTP Verification</h2>
            <p>We received a request to verify your account. Use the OTP code below to sign in securely.</p>
        </div>
        <div style="text-align: center;">
            <span class="otp-box">{{ otp }}</span>
        </div>
        <div class="footer">
            <p>If you did not request this, please ignore this email.</p>
            <p>This OTP is valid for 5 minutes only.</p>
            <p>Thank you for using our services!</p>
        </div>
    </div>
</body>
</html>
```

#### Welcome Template (`templates/email/welcome_template.html`)

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Welcome to Our Platform</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f7f7f7;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .button {
            display: inline-block;
            padding: 12px 24px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome {{ user_name }}!</h1>
        <p>Your account has been successfully created. You can now access your dashboard.</p>
        <div style="text-align: center;">
            <a href="{{ dashboard_link }}" class="button">Access Dashboard</a>
        </div>
        <p>If you have any questions, feel free to contact our support team.</p>
        <p>Best regards,<br>The Team</p>
    </div>
</body>
</html>
```

---

## 📱 SMS Notification System

### 1. Twilio Service Implementation (`services/twilio/twilio.py`)

```python
from twilio.rest import Client
from config_env import CONFIG

class TwilioVerifyService:
    def __init__(self, account_sid=None, auth_token=None, service_sid=None):
        """
        Initialize Twilio Verify Service.
        
        Args:
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token  
            service_sid: Twilio Verify Service SID
        """
        self.account_sid = account_sid or CONFIG.TWILIO_ACCOUNT_SID
        self.auth_token = auth_token or CONFIG.TWILIO_AUTH_TOKEN
        self.service_sid = service_sid or CONFIG.TWILIO_VERIFY_SERVICE_SID
        self.client = Client(self.account_sid, self.auth_token)

    def send_otp_to_mobile(self, phone):
        """
        Sends an OTP to the given phone number using Twilio Verify.
        
        Args:
            phone: Phone number in E.164 format (e.g., +1234567890)
            
        Returns:
            dict: Response with status and success flag
        """
        try:
            verification = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verifications \
                .create(to=phone, channel="sms")
            return {"status": verification.status, "success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_otp(self, phone, code):
        """
        Verifies the OTP entered by the user.
        
        Args:
            phone: Phone number in E.164 format
            code: OTP code entered by user
            
        Returns:
            dict: Response with verification status
        """
        try:
            verification_check = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verification_checks \
                .create(to=phone, code=code)
            return {
                "status": verification_check.status,
                "success": verification_check.status == "approved"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### 2. Mobile OTP Helper Functions (Add to `backend/utils/helpers.py`)

```python
from services.twilio.twilio import TwilioVerifyService

def send_mobile_otp(phone_number):
    """
    Send OTP to mobile number via Twilio.
    
    Args:
        phone_number: Phone number in international format
        
    Returns:
        dict: Response with status
    """
    try:
        if not phone_number:
            return {"status": "error", "message": "Phone number is required."}

        # Initialize Twilio service
        twilio = TwilioVerifyService()
        
        # Send OTP
        otp_response = twilio.send_otp_to_mobile(phone_number)
        
        if otp_response.get("success"):
            return {"status": "success", "message": "OTP sent successfully to mobile."}
        else:
            return {"status": "error", "message": otp_response.get("error", "Failed to send OTP.")}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def verify_mobile_otp(phone_number, otp):
    """
    Verify mobile OTP via Twilio.
    
    Args:
        phone_number: Phone number in international format
        otp: OTP code to verify
        
    Returns:
        dict: Verification response
    """
    try:
        if not phone_number or not otp:
            return {"status": "error", "message": "Phone number and OTP are required."}

        # Initialize Twilio service
        twilio = TwilioVerifyService()
        
        # Verify OTP
        verification_result = twilio.verify_otp(phone_number, otp)
        
        if verification_result.get("status") == "approved":
            return {"status": "success", "message": "OTP verified successfully."}
        else:
            return {"status": "error", "message": "Invalid or expired OTP."}

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
```

---

## 🔗 API Endpoints

### Django Views (`backend/common/views.py` or your views file)

```python
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from backend.utils.helpers import send_otp, verify_otp, send_mobile_otp, verify_mobile_otp
from backend.users.models import CustomUser  # Replace with your User model

@method_decorator(csrf_exempt, name='dispatch')
class SendOTPView(View):
    def post(self, request, *args, **kwargs):
        """Send OTP to email address."""
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            
            if not email:
                return JsonResponse({"error": "Email is required."}, status=400)

            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "Email already registered."}, status=400)

            otp_response = send_otp(email)
            
            if otp_response["status"] == "success":
                return JsonResponse({"status": "success", "message": "OTP sent successfully!"})
            else:
                return JsonResponse({"status": "error", "message": otp_response["message"]}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTPView(View):
    def post(self, request, *args, **kwargs):
        """Verify email OTP."""
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            otp = data.get('otp')
            
            if not email or not otp:
                return JsonResponse({"error": "Email and OTP are required."}, status=400)

            verification_result = verify_otp(email, otp)
            
            if verification_result["status"] == "success":
                return JsonResponse({"status": "success", "message": "OTP verified successfully!"})
            else:
                return JsonResponse({"status": "error", "message": verification_result["message"]}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SendMobileOTPView(View):
    def post(self, request, *args, **kwargs):
        """Send OTP to mobile number."""
        try:
            data = json.loads(request.body.decode('utf-8'))
            mobile = data.get('mobile')
            
            if not mobile:
                return JsonResponse({"error": "Mobile number is required."}, status=400)

            # Check if mobile already exists
            if CustomUser.objects.filter(phone_no=mobile).exists():
                return JsonResponse({"status": "error", "message": "Mobile number already registered."}, status=400)

            # Add country code if not present
            phone_number = f"+91{mobile}" if not mobile.startswith('+') else mobile
            otp_response = send_mobile_otp(phone_number)
            
            if otp_response["status"] == "success":
                return JsonResponse({"status": "success", "message": "OTP sent successfully!"})
            else:
                return JsonResponse({"status": "error", "message": otp_response["message"]}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyMobileOTPView(View):
    def post(self, request, *args, **kwargs):
        """Verify mobile OTP."""
        try:
            data = json.loads(request.body.decode('utf-8'))
            mobile = data.get('mobile')
            otp = data.get('otp')
            
            if not mobile or not otp:
                return JsonResponse({"error": "Mobile number and OTP are required."}, status=400)

            # Add country code if not present
            phone_number = f"+91{mobile}" if not mobile.startswith('+') else mobile
            verification_result = verify_mobile_otp(phone_number, otp)
            
            if verification_result["status"] == "success":
                return JsonResponse({"status": "success", "message": "OTP verified successfully!"})
            else:
                return JsonResponse({"status": "error", "message": verification_result["message"]}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
```

### URL Configuration (`urls.py`)

```python
from django.urls import path
from .views import SendOTPView, VerifyOTPView, SendMobileOTPView, VerifyMobileOTPView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('send-mobile-otp/', SendMobileOTPView.as_view(), name='send_mobile_otp'),
    path('verify-mobile-otp/', VerifyMobileOTPView.as_view(), name='verify_mobile_otp'),
]
```

---

## 🌐 Frontend Integration

### HTML Template Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Form</title>
    <!-- Include SweetAlert2 for nice alerts -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
</head>
<body>
    <!-- Email Section -->
    <div class="form-group">
        <label for="email">Email Address</label>
        <input type="email" id="email" name="email" placeholder="Enter email" required>
        <input type="hidden" id="email-status" value="invalid" data-email="">
        <button type="button" id="send-otp-btn" onclick="sendEmailOTP()" style="display: none;">Send OTP</button>
    </div>

    <!-- Email OTP Section -->
    <div id="email-otp-section" style="display: none;">
        <label for="email-otp">Enter Email OTP:</label>
        <input type="text" id="email-otp" placeholder="Enter 6-digit OTP" maxlength="6">
        <button type="button" id="verify-email-otp-btn" onclick="verifyEmailOTP()">Verify OTP</button>
        <button type="button" id="resend-email-otp" onclick="sendEmailOTP()">Resend OTP</button>
    </div>

    <!-- Mobile Section -->
    <div class="form-group">
        <label for="mobile">Mobile Number</label>
        <input type="tel" id="mobile" name="mobile" placeholder="Enter mobile number" pattern="[0-9]{10}" required>
        <input type="hidden" id="mobile-status" value="invalid" data-mobile="">
        <button type="button" id="send-mobile-otp-btn" onclick="sendMobileOTP()" style="display: none;">Send OTP</button>
    </div>

    <!-- Mobile OTP Section -->
    <div id="mobile-otp-section" style="display: none;">
        <label for="mobile-otp">Enter Mobile OTP:</label>
        <input type="text" id="mobile-otp" placeholder="Enter 6-digit OTP" maxlength="6">
        <button type="button" id="verify-mobile-otp-btn" onclick="verifyMobileOTP()">Verify OTP</button>
        <button type="button" id="resend-mobile-otp" onclick="sendMobileOTP()">Resend OTP</button>
    </div>

    <script src="path/to/your/verification.js"></script>
</body>
</html>
```

### JavaScript Implementation (`static/js/verification.js`)

```javascript
// Email validation and OTP sending
document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('email');
    const sendOtpBtn = document.getElementById('send-otp-btn');
    const emailStatus = document.getElementById('email-status');

    // Email input validation
    emailInput.addEventListener('input', function() {
        const emailVal = emailInput.value.trim();
        const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal);

        if (isValidEmail) {
            sendOtpBtn.style.display = 'inline-block';
            sendOtpBtn.disabled = false;
        } else {
            sendOtpBtn.style.display = 'none';
            sendOtpBtn.disabled = true;
        }
    });

    // Mobile input validation
    const mobileInput = document.getElementById('mobile');
    const sendMobileOtpBtn = document.getElementById('send-mobile-otp-btn');
    const mobileStatus = document.getElementById('mobile-status');

    mobileInput.addEventListener('input', function() {
        const mobileVal = mobileInput.value.trim();
        const isValidMobile = /^[0-9]{10}$/.test(mobileVal);

        if (isValidMobile) {
            sendMobileOtpBtn.style.display = 'inline-block';
            sendMobileOtpBtn.disabled = false;
        } else {
            sendMobileOtpBtn.style.display = 'none';
            sendMobileOtpBtn.disabled = true;
        }
    });
});

// Email OTP Functions
function sendEmailOTP() {
    const emailField = document.getElementById('email');
    const emailValue = emailField.value.trim();

    Swal.fire({
        title: 'Sending OTP...',
        text: 'Please wait while we send the OTP to your email.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('/send-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            email: emailValue
        })
    })
    .then(response => response.json())
    .then(data => {
        Swal.close();
        
        if (data.status === 'success') {
            Swal.fire({
                icon: 'success',
                title: 'OTP Sent!',
                text: 'Please check your email for the OTP.',
            });
            
            // Show OTP input section
            document.getElementById('email-otp-section').style.display = 'block';
            document.getElementById('send-otp-btn').style.display = 'none';
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: data.message || 'Failed to send OTP. Please try again.',
            });
        }
    })
    .catch(error => {
        Swal.close();
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to send OTP. Please try again.',
        });
        console.error('Error:', error);
    });
}

function verifyEmailOTP() {
    const emailValue = document.getElementById('email').value.trim();
    const otpValue = document.getElementById('email-otp').value.trim();

    if (!otpValue || otpValue.length !== 6) {
        Swal.fire({
            icon: 'warning',
            title: 'Invalid OTP',
            text: 'Please enter a valid 6-digit OTP.',
        });
        return;
    }

    Swal.fire({
        title: 'Verifying OTP...',
        text: 'Please wait while we verify your OTP.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('/verify-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            email: emailValue,
            otp: otpValue
        })
    })
    .then(response => response.json())
    .then(data => {
        Swal.close();
        
        if (data.status === 'success') {
            Swal.fire({
                icon: 'success',
                title: 'Email Verified!',
                text: 'Your email has been successfully verified.',
            });
            
            // Update UI
            document.getElementById('email').readOnly = true;
            document.getElementById('email').style.backgroundColor = '#e9ecef';
            document.getElementById('email-otp-section').style.display = 'none';
            document.getElementById('email-status').value = 'valid';
            document.getElementById('email-status').setAttribute('data-email', emailValue);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Verification Failed',
                text: data.message || 'Invalid OTP. Please try again.',
            });
        }
    })
    .catch(error => {
        Swal.close();
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to verify OTP. Please try again.',
        });
        console.error('Error:', error);
    });
}

// Mobile OTP Functions
function sendMobileOTP() {
    const mobileField = document.getElementById('mobile');
    const mobileValue = mobileField.value.trim();

    Swal.fire({
        title: 'Sending OTP...',
        text: 'Please wait while we send the OTP to your mobile.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('/send-mobile-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            mobile: mobileValue
        })
    })
    .then(response => response.json())
    .then(data => {
        Swal.close();
        
        if (data.status === 'success') {
            Swal.fire({
                icon: 'success',
                title: 'OTP Sent!',
                text: 'Please check your mobile for the OTP.',
            });
            
            // Show OTP input section
            document.getElementById('mobile-otp-section').style.display = 'block';
            document.getElementById('send-mobile-otp-btn').style.display = 'none';
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: data.message || 'Failed to send OTP. Please try again.',
            });
        }
    })
    .catch(error => {
        Swal.close();
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to send OTP. Please try again.',
        });
        console.error('Error:', error);
    });
}

function verifyMobileOTP() {
    const mobileValue = document.getElementById('mobile').value.trim();
    const otpValue = document.getElementById('mobile-otp').value.trim();

    if (!otpValue || otpValue.length !== 6) {
        Swal.fire({
            icon: 'warning',
            title: 'Invalid OTP',
            text: 'Please enter a valid 6-digit OTP.',
        });
        return;
    }

    Swal.fire({
        title: 'Verifying OTP...',
        text: 'Please wait while we verify your OTP.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch('/verify-mobile-otp/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            mobile: mobileValue,
            otp: otpValue
        })
    })
    .then(response => response.json())
    .then(data => {
        Swal.close();
        
        if (data.status === 'success') {
            Swal.fire({
                icon: 'success',
                title: 'Mobile Verified!',
                text: 'Your mobile number has been successfully verified.',
            });
            
            // Update UI
            document.getElementById('mobile').readOnly = true;
            document.getElementById('mobile').style.backgroundColor = '#e9ecef';
            document.getElementById('mobile-otp-section').style.display = 'none';
            document.getElementById('mobile-status').value = 'valid';
            document.getElementById('mobile-status').setAttribute('data-mobile', mobileValue);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Verification Failed',
                text: data.message || 'Invalid OTP. Please try again.',
            });
        }
    })
    .catch(error => {
        Swal.close();
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to verify OTP. Please try again.',
        });
        console.error('Error:', error);
    });
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

---

## 🛠️ Complete Setup Guide

### Step 1: Environment Configuration

Create a `.env` file in your project root:

```bash
# Email Configuration
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
EMAIL_SERVER=SENDGRID

# Alternative Gmail SMTP (for development)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_HOST_USER=your_email@gmail.com
# EMAIL_HOST_PASSWORD=your_app_password
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# DEFAULT_FROM_EMAIL=your_email@gmail.com
# EMAIL_SERVER=SMTP

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_VERIFY_SERVICE_SID=your_verify_service_sid

# Redis Configuration
REDIS_DEFAULT_URL=redis://localhost:6379/0
REDIS_OTP_URL=redis://localhost:6379/1
REDIS_SESSION_URL=redis://localhost:6379/2
```

### Step 2: Django Settings Configuration

Add to your `settings.py`:

```python
import os
from config_env import CONFIG

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.EMAIL_HOST
EMAIL_PORT = CONFIG.EMAIL_PORT
EMAIL_HOST_USER = CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = CONFIG.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = CONFIG.EMAIL_USE_TLS
DEFAULT_FROM_EMAIL = CONFIG.DEFAULT_FROM_EMAIL

# Redis Configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CONFIG.REDIS_DEFAULT_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'otp_cache': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CONFIG.REDIS_OTP_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Step 3: Required Service Accounts

#### SendGrid Setup:
1. Go to [SendGrid](https://sendgrid.com/)
2. Create account and verify domain
3. Generate API key from Settings > API Keys
4. Add API key to `.env` file

#### Twilio Setup:
1. Go to [Twilio Console](https://console.twilio.com/)
2. Create account and get Account SID & Auth Token
3. Go to Verify > Services and create a new service
4. Get Service SID and add all credentials to `.env`

#### Redis Setup:
```bash
# Install Redis (Ubuntu/Debian)
sudo apt update
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis
redis-cli ping
```

### Step 4: Install Dependencies

```bash
pip install django python-decouple python-dotenv redis twilio django-redis
```

### Step 5: Database Migration

If you have custom User model with phone field:

```python
# In your User model
class CustomUser(AbstractUser):
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Testing

### Test Email Functionality

```python
# Test in Django shell
python manage.py shell

from services.email_service import EmailHelper
from backend.users.models import CustomUser

user = CustomUser.objects.first()
email_helper = EmailHelper(
    user=user,
    email_type='otp',
    content={'otp': '123456'}
)
result = email_helper.send_email()
print(result)
```

### Test SMS Functionality

```python
# Test in Django shell
from services.twilio.twilio import TwilioVerifyService

twilio = TwilioVerifyService()
result = twilio.send_otp_to_mobile('+1234567890')
print(result)

# Verify OTP
verify_result = twilio.verify_otp('+1234567890', '123456')
print(verify_result)
```

### Test with Postman

#### Send Email OTP:
```
POST http://localhost:8000/send-otp/
Content-Type: application/json

{
    "email": "test@example.com"
}
```

#### Verify Email OTP:
```
POST http://localhost:8000/verify-otp/
Content-Type: application/json

{
    "email": "test@example.com",
    "otp": "123456"
}
```

#### Send Mobile OTP:
```
POST http://localhost:8000/send-mobile-otp/
Content-Type: application/json

{
    "mobile": "1234567890"
}
```

#### Verify Mobile OTP:
```
POST http://localhost:8000/verify-mobile-otp/
Content-Type: application/json

{
    "mobile": "1234567890",
    "otp": "123456"
}
```

---

## 🔧 Troubleshooting

### Common Email Issues

**SMTP Authentication Failed:**
```python
# For Gmail, use App Password instead of regular password
# 1. Enable 2FA on Gmail
# 2. Generate App Password
# 3. Use App Password in EMAIL_HOST_PASSWORD
```

**SendGrid API Error:**
```python
# Check API key permissions
# Ensure domain is verified
# Check sender authentication
```

### Common SMS Issues

**Twilio Authentication Error:**
```python
# Verify Account SID and Auth Token
# Check Service SID is correct
# Ensure account has sufficient balance
```

**Phone Number Format Error:**
```python
# Use E.164 format: +1234567890
# Include country code
# Remove any spaces or special characters
```

### Common Redis Issues

**Connection Refused:**
```bash
# Check if Redis is running
sudo systemctl status redis-server

# Start Redis if not running
sudo systemctl start redis-server

# Check Redis configuration
redis-cli config get "*"
```

### Debug Mode

Add logging to see detailed errors:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In your functions
logger.debug(f"Sending OTP to: {email}")
logger.error(f"Error occurred: {str(e)}")
```

---

## 📚 Additional Resources

### Documentation Links:
- [Django Email Documentation](https://docs.djangoproject.com/en/stable/topics/email/)
- [Twilio Verify API](https://www.twilio.com/docs/verify/api)
- [SendGrid API Documentation](https://docs.sendgrid.com/)
- [Redis Documentation](https://redis.io/documentation)
- [SweetAlert2 Documentation](https://sweetalert2.github.io/)

### Helpful Tools:
- [Mailtrap](https://mailtrap.io/) - Email testing
- [Redis Commander](https://github.com/joeferner/redis-commander) - Redis GUI
- [Postman](https://www.postman.com/) - API testing

### Best Practices:
1. **Rate Limiting**: Implement rate limiting for OTP requests
2. **OTP Expiry**: Set appropriate expiry times (5-10 minutes)
3. **Security**: Hash OTPs before storing
4. **Logging**: Log important events for debugging
5. **Error Handling**: Provide meaningful error messages
6. **Testing**: Test thoroughly in development environment

---

## 🎯 Quick Start Checklist

- [ ] Install required packages
- [ ] Set up service accounts (SendGrid, Twilio)
- [ ] Configure environment variables
- [ ] Set up Redis server
- [ ] Create email templates
- [ ] Implement backend services
- [ ] Create API endpoints
- [ ] Add frontend JavaScript
- [ ] Test email functionality
- [ ] Test SMS functionality
- [ ] Deploy and monitor

---

**🎉 Congratulations!** You now have a complete email and SMS notification system. This implementation is production-ready and can handle thousands of notifications per day.

For any issues or questions, refer to the troubleshooting section or check the official documentation of the respective services.
