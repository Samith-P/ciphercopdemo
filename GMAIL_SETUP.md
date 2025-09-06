# Gmail SMTP Setup Guide

## 🚨 Important: Gmail Authentication Error Fix

If you're getting the error `Username and Password not accepted`, follow these steps exactly:

## Step 1: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Under "Signing in to Google", click on "2-Step Verification"
3. Follow the setup process to enable 2FA (required for App Passwords)

## Step 2: Generate App Password

1. After enabling 2FA, go back to [Security Settings](https://myaccount.google.com/security)
2. Under "Signing in to Google", click on "App passwords"
3. Select "Mail" as the app
4. Select "Other (Custom name)" as the device
5. Enter "Flask Notification App" as the name
6. Click "Generate"
7. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

## Step 3: Update Your .env File

Update your `.env` file with these settings:

```env
# Gmail SMTP Configuration
GMAIL_USER=your-actual-email@gmail.com
GMAIL_PASSWORD=abcd efgh ijkl mnop

# Make sure these match for default config
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-actual-email@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=your-actual-email@gmail.com
```

## Step 4: Test Your Setup

1. Restart your Flask application
2. In the web interface, select "Gmail SMTP" from the dropdown
3. Click "Test Gmail Connection" button
4. If successful, try sending a test email

## Common Issues & Solutions

### Issue: "Username and Password not accepted"
- **Solution**: Use App Password, not your regular Gmail password
- Make sure 2FA is enabled first

### Issue: "Less secure app access"
- **Solution**: This is outdated. Use App Passwords instead

### Issue: "Connection timeout"
- **Solution**: Check your firewall/antivirus settings
- Make sure port 587 is not blocked

### Issue: "App Password not working"
- **Solution**: Remove spaces from the App Password
- Use the full 16-character password exactly as generated

## Security Notes

- ✅ App Passwords are more secure than regular passwords
- ✅ You can revoke App Passwords anytime
- ✅ Each app should have its own App Password
- ❌ Never share your App Password
- ❌ Don't use your regular Gmail password for SMTP

## Testing Checklist

- [ ] 2-Factor Authentication enabled
- [ ] App Password generated
- [ ] .env file updated with correct credentials
- [ ] Flask app restarted
- [ ] "Test Gmail Connection" button works
- [ ] Test email sent successfully

## Alternative: Use Mailtrap for Testing

If you just want to test the app without setting up Gmail:

1. Create free account at [Mailtrap.io](https://mailtrap.io)
2. Get your SMTP credentials from inbox settings
3. Select "Mailtrap" in the email service dropdown
4. Emails will appear in Mailtrap inbox (not real delivery)

## Need Help?

1. Check the browser console for detailed error messages
2. Look at the Flask terminal output for debugging info
3. Use the "Test Gmail Connection" feature to diagnose issues
4. Verify your .env file format matches the example exactly
