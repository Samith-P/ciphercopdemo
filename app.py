from flask import Flask, render_template, request, jsonify
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import os
from dotenv import load_dotenv
import random
import string
import redis
import json
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
class Config:
    # Email Settings
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER', 'your-email@gmail.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-app-password')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'no-reply@example.com')
    
    # Twilio Settings
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_VERIFY_SERVICE_SID = os.getenv('TWILIO_VERIFY_SERVICE_SID', '')
    
    # Redis Settings (Optional - for OTP storage)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Initialize Redis (optional)
try:
    redis_client = redis.from_url(Config.REDIS_URL)
    redis_available = True
except:
    redis_available = False
    # Use in-memory storage as fallback
    otp_storage = {}

def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))

def store_otp(email_or_phone, otp, expiry_minutes=5):
    """Store OTP with expiry"""
    if redis_available:
        redis_client.setex(f"otp:{email_or_phone}", expiry_minutes * 60, otp)
    else:
        expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
        otp_storage[email_or_phone] = {'otp': otp, 'expiry': expiry_time}

def verify_otp(email_or_phone, entered_otp):
    """Verify OTP"""
    if redis_available:
        stored_otp = redis_client.get(f"otp:{email_or_phone}")
        if stored_otp and stored_otp.decode('utf-8') == entered_otp:
            redis_client.delete(f"otp:{email_or_phone}")
            return True
    else:
        if email_or_phone in otp_storage:
            stored_data = otp_storage[email_or_phone]
            if (stored_data['otp'] == entered_otp and 
                datetime.now() < stored_data['expiry']):
                del otp_storage[email_or_phone]
                return True
            elif datetime.now() >= stored_data['expiry']:
                del otp_storage[email_or_phone]
    return False

def send_email(to_email, subject, message, is_html=False, email_service=None):
    """Send email using SMTP with dynamic service selection"""
    try:
        # Determine email configuration based on service selection
        if email_service == 'gmail':
            email_host = 'smtp.gmail.com'
            email_port = 587
            email_user = os.getenv('GMAIL_USER', Config.EMAIL_USER)
            email_password = os.getenv('GMAIL_PASSWORD', Config.EMAIL_PASSWORD)
            from_email = email_user
            service_name = "Gmail SMTP"
        elif email_service == 'mailtrap':
            email_host = os.getenv('MAILTRAP_HOST', 'sandbox.smtp.mailtrap.io')
            email_port = int(os.getenv('MAILTRAP_PORT', '2525'))
            email_user = os.getenv('MAILTRAP_USER', Config.EMAIL_USER)
            email_password = os.getenv('MAILTRAP_PASSWORD', Config.EMAIL_PASSWORD)
            from_email = os.getenv('MAILTRAP_FROM', Config.FROM_EMAIL)
            service_name = "Mailtrap Testing"
        else:
            # Use default configuration
            email_host = Config.EMAIL_HOST
            email_port = Config.EMAIL_PORT
            email_user = Config.EMAIL_USER
            email_password = Config.EMAIL_PASSWORD
            from_email = Config.FROM_EMAIL
            service_name = "Default SMTP"
        
        print(f"[EMAIL DEBUG] Sending email via {service_name} ({email_host}:{email_port})")
        print(f"[EMAIL DEBUG] From: {from_email}")
        print(f"[EMAIL DEBUG] To: {to_email}")
        print(f"[EMAIL DEBUG] Subject: {subject}")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Add content
        if is_html:
            msg.attach(MIMEText(message, 'html'))
        else:
            msg.attach(MIMEText(message, 'plain'))
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls(context=context)
            server.login(email_user, email_password)
            server.send_message(msg)
        
        print(f"[EMAIL DEBUG] Email sent successfully via {service_name}!")
        
        # Add service-specific info to response
        if email_service == 'mailtrap':
            service_info = " via Mailtrap (Check your Mailtrap inbox - emails are not delivered to real addresses)"
        elif email_service == 'gmail':
            service_info = " via Gmail SMTP (Check the recipient's real inbox)"
        else:
            service_info = f" via {service_name}"
        
        return {"success": True, "message": f"Email sent successfully{service_info}"}
    except smtplib.SMTPAuthenticationError as e:
        error_msg = str(e)
        print(f"[EMAIL DEBUG] SMTP Authentication failed: {error_msg}")
        
        if email_service == 'gmail' or 'gmail' in email_host.lower():
            detailed_msg = (
                "Gmail authentication failed. Please check:\n"
                "1. Use your Gmail address (not username)\n"
                "2. Use App Password (not regular password)\n"
                "3. Enable 2-Factor Authentication first\n"
                "4. Generate App Password: Google Account → Security → App passwords\n"
                "5. Update GMAIL_USER and GMAIL_PASSWORD in .env file"
            )
        else:
            detailed_msg = f"SMTP Authentication failed for {service_name}. Please check your credentials."
            
        return {"success": False, "message": detailed_msg}
    except Exception as e:
        print(f"[EMAIL DEBUG] Failed to send email: {str(e)}")
        return {"success": False, "message": f"Failed to send email: {str(e)}"}

def send_sms_otp(phone_number):
    """Send SMS OTP using Twilio Verify"""
    try:
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        verification = client.verify \
            .v2 \
            .services(Config.TWILIO_VERIFY_SERVICE_SID) \
            .verifications \
            .create(to=phone_number, channel='sms')
        
        return {"success": True, "message": "SMS OTP sent successfully", "status": verification.status}
    except Exception as e:
        return {"success": False, "message": f"Failed to send SMS: {str(e)}"}

def verify_sms_otp(phone_number, otp_code):
    """Verify SMS OTP using Twilio"""
    try:
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        verification_check = client.verify \
            .v2 \
            .services(Config.TWILIO_VERIFY_SERVICE_SID) \
            .verification_checks \
            .create(to=phone_number, code=otp_code)
        
        return {
            "success": verification_check.status == "approved",
            "status": verification_check.status
        }
    except Exception as e:
        return {"success": False, "message": f"Failed to verify SMS OTP: {str(e)}"}

# Routes
@app.route('/')
def index():
    """Main page with notification forms"""
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email_route():
    """Send email notification"""
    try:
        data = request.get_json()
        to_email = data.get('email')
        subject = data.get('subject', 'Test Email')
        message = data.get('message', 'This is a test email')
        email_service = data.get('email_service', None)  # Get selected email service
        
        if not to_email:
            return jsonify({"success": False, "message": "Email address is required"})
        
        result = send_email(to_email, subject, message, email_service=email_service)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/send_email_otp', methods=['POST'])
def send_email_otp_route():
    """Send email OTP"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({"success": False, "message": "Email address is required"})
        
        # Generate OTP
        otp = generate_otp()
        
        # Store OTP
        store_otp(email, otp)
        
        # Create HTML email
        html_message = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f7f7f7;">
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; text-align: center;">Email Verification</h2>
                    <p style="color: #666; font-size: 16px;">Your OTP for email verification is:</p>
                    <div style="text-align: center; margin: 20px 0;">
                        <span style="font-size: 32px; font-weight: bold; color: #007bff; background-color: #f8f9fa; padding: 10px 20px; border-radius: 5px; letter-spacing: 3px;">{otp}</span>
                    </div>
                    <p style="color: #666; font-size: 14px;">This OTP is valid for 5 minutes.</p>
                    <p style="color: #666; font-size: 14px;">If you didn't request this, please ignore this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        result = send_email(email, "Your Email Verification OTP", html_message, is_html=True)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/verify_email_otp', methods=['POST'])
def verify_email_otp_route():
    """Verify email OTP"""
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return jsonify({"success": False, "message": "Email and OTP are required"})
        
        if verify_otp(email, otp):
            return jsonify({"success": True, "message": "Email OTP verified successfully"})
        else:
            return jsonify({"success": False, "message": "Invalid or expired OTP"})
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/send_sms', methods=['POST'])
def send_sms_route():
    """Send SMS OTP"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone:
            return jsonify({"success": False, "message": "Phone number is required"})
        
        # Ensure phone number is in international format
        if not phone.startswith('+'):
            phone = f'+91{phone}'  # Default to India, adjust as needed
        
        result = send_sms_otp(phone)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/verify_sms', methods=['POST'])
def verify_sms_route():
    """Verify SMS OTP"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        otp = data.get('otp')
        
        if not phone or not otp:
            return jsonify({"success": False, "message": "Phone number and OTP are required"})
        
        # Ensure phone number is in international format
        if not phone.startswith('+'):
            phone = f'+91{phone}'
        
        result = verify_sms_otp(phone, otp)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/config')
def config_status():
    """Check configuration status"""
    # Determine email service type
    email_service_type = "Unknown"
    if "mailtrap" in Config.EMAIL_HOST.lower():
        email_service_type = "Mailtrap (Testing)"
    elif "gmail" in Config.EMAIL_HOST.lower():
        email_service_type = "Gmail SMTP (Real)"
    elif "sendgrid" in Config.EMAIL_HOST.lower():
        email_service_type = "SendGrid (Real)"
    else:
        email_service_type = f"SMTP ({Config.EMAIL_HOST})"
    
    # Check Gmail specific configuration
    gmail_user = os.getenv('GMAIL_USER', '')
    gmail_password = os.getenv('GMAIL_PASSWORD', '')
    gmail_configured = bool(gmail_user and gmail_password)
    
    # Check Mailtrap specific configuration  
    mailtrap_user = os.getenv('MAILTRAP_USER', '')
    mailtrap_password = os.getenv('MAILTRAP_PASSWORD', '')
    mailtrap_configured = bool(mailtrap_user and mailtrap_password)
    
    config_status = {
        "email_configured": bool(Config.EMAIL_USER and Config.EMAIL_PASSWORD),
        "email_service": email_service_type,
        "email_host": Config.EMAIL_HOST,
        "gmail_configured": gmail_configured,
        "mailtrap_configured": mailtrap_configured,
        "twilio_configured": bool(Config.TWILIO_ACCOUNT_SID and Config.TWILIO_AUTH_TOKEN),
        "redis_available": redis_available,
        # Debug info for Gmail setup
        "gmail_setup_info": {
            "has_gmail_user": bool(gmail_user),
            "gmail_user_format": gmail_user.endswith('@gmail.com') if gmail_user else False,
            "has_gmail_password": bool(gmail_password),
            "password_length": len(gmail_password) if gmail_password else 0
        }
    }
    return jsonify(config_status)

@app.route('/test_gmail_connection', methods=['POST'])
def test_gmail_connection():
    """Test Gmail SMTP connection without sending email"""
    try:
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_PASSWORD')
        
        if not gmail_user or not gmail_password:
            return jsonify({
                "success": False, 
                "message": "Gmail credentials not found in environment variables"
            })
        
        print(f"[GMAIL TEST] Testing connection for: {gmail_user}")
        
        # Test connection
        context = ssl.create_default_context()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=context)
            server.login(gmail_user, gmail_password)
        
        print(f"[GMAIL TEST] Connection successful!")
        return jsonify({
            "success": True, 
            "message": f"Gmail SMTP connection successful for {gmail_user}"
        })
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"[GMAIL TEST] Authentication failed: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Gmail authentication failed. Check your App Password setup.",
            "details": str(e)
        })
    except Exception as e:
        print(f"[GMAIL TEST] Connection failed: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Gmail connection test failed: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
