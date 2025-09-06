// Notification System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
    setupEventListeners();
    checkConfiguration();
});

function initializeApp() {
    addLog('Application initialized', 'info');
    addLog('Setting up event listeners...', 'info');
    
    // Initialize email service selector
    const emailService = document.getElementById('email-service');
    if (emailService) {
        emailService.value = 'gmail'; // Default to Gmail
        // Wait a bit for the DOM to be fully ready, then trigger the change
        setTimeout(() => {
            handleEmailServiceChange();
        }, 100);
    }
}

function setupEventListeners() {
    // Email form submission
    document.getElementById('email-form').addEventListener('submit', handleEmailSubmit);
    
    // Email service selection change
    document.getElementById('email-service').addEventListener('change', handleEmailServiceChange);
    
    // Email OTP buttons
    document.getElementById('send-email-otp-btn').addEventListener('click', sendEmailOTP);
    document.getElementById('verify-email-otp-btn').addEventListener('click', verifyEmailOTP);
    
    // SMS OTP buttons
    document.getElementById('send-sms-otp-btn').addEventListener('click', sendSMSOTP);
    document.getElementById('verify-sms-otp-btn').addEventListener('click', verifySMSOTP);
    
    // Clear logs button
    document.getElementById('clear-logs-btn').addEventListener('click', clearLogs);
    
    // Auto-format phone number
    document.getElementById('sms-phone').addEventListener('input', formatPhoneNumber);
    
    // Real-time validation
    document.getElementById('email-to').addEventListener('input', validateEmail);
    document.getElementById('email-otp-to').addEventListener('input', validateEmail);
}

function checkConfiguration() {
    addLog('Checking service configurations...', 'info');
    
    fetch('/config')
        .then(response => response.json())
        .then(data => {
            updateConfigStatus('email', data.email_configured);
            updateConfigStatus('sms', data.twilio_configured);
            updateConfigStatus('redis', data.redis_available);
            
            // Show email service info
            if (data.email_service) {
                const emailModeElement = document.getElementById('email-mode');
                if (emailModeElement) {
                    emailModeElement.textContent = data.email_service;
                    if (data.email_service.includes('Mailtrap')) {
                        emailModeElement.className = 'badge bg-warning ms-2';
                    } else if (data.email_service.includes('Gmail') || data.email_service.includes('Real')) {
                        emailModeElement.className = 'badge bg-success ms-2';
                    } else {
                        emailModeElement.className = 'badge bg-info ms-2';
                    }
                }
                
                addLog(`Email Service: ${data.email_service} (${data.email_host})`, 'info');
                
                // Add warning for Mailtrap
                if (data.email_service.includes('Mailtrap')) {
                    addLog('⚠️  Using Mailtrap: Emails will NOT be delivered to real addresses!', 'warning');
                    addLog('💡 To send real emails, configure Gmail SMTP in .env file', 'info');
                }
            }
            
            addLog('Configuration check completed', 'success');
        })
        .catch(error => {
            addLog('Failed to check configuration: ' + error.message, 'error');
        });
}

function updateConfigStatus(service, configured) {
    const statusElement = document.getElementById(`${service}-status`);
    const iconElement = document.getElementById(`${service}-status-icon`);
    
    if (configured) {
        statusElement.textContent = 'Configured';
        statusElement.className = 'badge bg-success ms-2';
        iconElement.className = iconElement.className.replace('text-muted', 'text-success');
    } else {
        statusElement.textContent = 'Not Configured';
        statusElement.className = 'badge bg-danger ms-2';
        iconElement.className = iconElement.className.replace('text-muted', 'text-danger');
    }
}

// Email Functions
function handleEmailSubmit(event) {
    event.preventDefault();
    
    const email = document.getElementById('email-to').value;
    const subject = document.getElementById('email-subject').value;
    const message = document.getElementById('email-message').value;
    const emailService = document.getElementById('email-service').value;
    
    if (!validateEmailAddress(email)) {
        showAlert('Please enter a valid email address', 'error');
        return;
    }
    
    sendEmail(email, subject, message, emailService);
}

function sendEmail(email, subject, message, emailService) {
    const button = event.target;
    setButtonLoading(button, true);
    
    addLog(`Sending email via ${emailService.toUpperCase()} to ${email}...`, 'info');
    
    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            subject: subject,
            message: message,
            email_service: emailService
        })
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(button, false);
        
        if (data.success) {
            showAlert('Email sent successfully!', 'success');
            addLog(`Email sent successfully to ${email}`, 'success');
            document.getElementById('email-form').reset();
        } else {
            showAlert('Failed to send email: ' + data.message, 'error');
            addLog(`Failed to send email: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        setButtonLoading(button, false);
        showAlert('Error sending email: ' + error.message, 'error');
        addLog(`Error sending email: ${error.message}`, 'error');
    });
}

function sendEmailOTP() {
    const email = document.getElementById('email-otp-to').value;
    const button = document.getElementById('send-email-otp-btn');
    
    if (!validateEmailAddress(email)) {
        showAlert('Please enter a valid email address', 'error');
        return;
    }
    
    setButtonLoading(button, true);
    addLog(`Sending email OTP to ${email}...`, 'info');
    
    fetch('/send_email_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(button, false);
        
        if (data.success) {
            showAlert('Email OTP sent successfully! Check your inbox.', 'success');
            addLog(`Email OTP sent to ${email}`, 'success');
            document.getElementById('email-otp-verify-section').style.display = 'block';
            document.getElementById('email-otp-to').readOnly = true;
        } else {
            showAlert('Failed to send email OTP: ' + data.message, 'error');
            addLog(`Failed to send email OTP: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        setButtonLoading(button, false);
        showAlert('Error sending email OTP: ' + error.message, 'error');
        addLog(`Error sending email OTP: ${error.message}`, 'error');
    });
}

function verifyEmailOTP() {
    const email = document.getElementById('email-otp-to').value;
    const otp = document.getElementById('email-otp-code').value;
    const button = document.getElementById('verify-email-otp-btn');
    
    if (!otp || otp.length !== 6) {
        showAlert('Please enter a valid 6-digit OTP', 'error');
        return;
    }
    
    setButtonLoading(button, true);
    addLog(`Verifying email OTP for ${email}...`, 'info');
    
    fetch('/verify_email_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, otp: otp })
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(button, false);
        
        if (data.success) {
            showAlert('Email OTP verified successfully!', 'success');
            addLog(`Email OTP verified for ${email}`, 'success');
            resetEmailOTPForm();
            markFieldAsSuccess('email-otp-to');
        } else {
            showAlert('Email OTP verification failed: ' + data.message, 'error');
            addLog(`Email OTP verification failed: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        setButtonLoading(button, false);
        showAlert('Error verifying email OTP: ' + error.message, 'error');
        addLog(`Error verifying email OTP: ${error.message}`, 'error');
    });
}

// SMS Functions
function sendSMSOTP() {
    const phone = document.getElementById('sms-phone').value;
    const button = document.getElementById('send-sms-otp-btn');
    
    if (!validatePhoneNumber(phone)) {
        showAlert('Please enter a valid 10-digit phone number', 'error');
        return;
    }
    
    setButtonLoading(button, true);
    addLog(`Sending SMS OTP to +91${phone}...`, 'info');
    
    fetch('/send_sms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone: phone })
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(button, false);
        
        if (data.success) {
            showAlert('SMS OTP sent successfully! Check your phone.', 'success');
            addLog(`SMS OTP sent to +91${phone}`, 'success');
            document.getElementById('sms-otp-verify-section').style.display = 'block';
            document.getElementById('sms-phone').readOnly = true;
        } else {
            showAlert('Failed to send SMS OTP: ' + data.message, 'error');
            addLog(`Failed to send SMS OTP: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        setButtonLoading(button, false);
        showAlert('Error sending SMS OTP: ' + error.message, 'error');
        addLog(`Error sending SMS OTP: ${error.message}`, 'error');
    });
}

function verifySMSOTP() {
    const phone = document.getElementById('sms-phone').value;
    const otp = document.getElementById('sms-otp-code').value;
    const button = document.getElementById('verify-sms-otp-btn');
    
    if (!otp || otp.length !== 6) {
        showAlert('Please enter a valid 6-digit OTP', 'error');
        return;
    }
    
    setButtonLoading(button, true);
    addLog(`Verifying SMS OTP for +91${phone}...`, 'info');
    
    fetch('/verify_sms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone: phone, otp: otp })
    })
    .then(response => response.json())
    .then(data => {
        setButtonLoading(button, false);
        
        if (data.success) {
            showAlert('SMS OTP verified successfully!', 'success');
            addLog(`SMS OTP verified for +91${phone}`, 'success');
            resetSMSOTPForm();
            markFieldAsSuccess('sms-phone');
        } else {
            showAlert('SMS OTP verification failed: ' + (data.message || 'Invalid OTP'), 'error');
            addLog(`SMS OTP verification failed: ${data.message || 'Invalid OTP'}`, 'error');
        }
    })
    .catch(error => {
        setButtonLoading(button, false);
        showAlert('Error verifying SMS OTP: ' + error.message, 'error');
        addLog(`Error verifying SMS OTP: ${error.message}`, 'error');
    });
}

// Utility Functions
function validateEmailAddress(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePhoneNumber(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone);
}

function validateEmail(event) {
    const input = event.target;
    const isValid = validateEmailAddress(input.value);
    
    if (input.value && !isValid) {
        input.classList.add('error-border');
        input.classList.remove('success-border');
    } else if (isValid) {
        input.classList.add('success-border');
        input.classList.remove('error-border');
    } else {
        input.classList.remove('error-border', 'success-border');
    }
}

function formatPhoneNumber(event) {
    const input = event.target;
    let value = input.value.replace(/\D/g, '');
    
    if (value.length > 10) {
        value = value.substring(0, 10);
    }
    
    input.value = value;
    
    const isValid = validatePhoneNumber(value);
    if (value && !isValid) {
        input.classList.add('error-border');
        input.classList.remove('success-border');
    } else if (isValid) {
        input.classList.add('success-border');
        input.classList.remove('error-border');
    } else {
        input.classList.remove('error-border', 'success-border');
    }
}

function setButtonLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.classList.add('btn-loading');
        button.originalText = button.innerHTML;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    } else {
        button.disabled = false;
        button.classList.remove('btn-loading');
        button.innerHTML = button.originalText;
    }
}

function markFieldAsSuccess(fieldId) {
    const field = document.getElementById(fieldId);
    field.classList.add('success-border');
    field.classList.remove('error-border');
}

function resetEmailOTPForm() {
    document.getElementById('email-otp-verify-section').style.display = 'none';
    document.getElementById('email-otp-to').readOnly = false;
    document.getElementById('email-otp-code').value = '';
}

function resetSMSOTPForm() {
    document.getElementById('sms-otp-verify-section').style.display = 'none';
    document.getElementById('sms-phone').readOnly = false;
    document.getElementById('sms-otp-code').value = '';
}

function showAlert(message, type) {
    const config = {
        title: type === 'success' ? 'Success!' : type === 'error' ? 'Error!' : 'Info',
        text: message,
        icon: type === 'success' ? 'success' : type === 'error' ? 'error' : 'info',
        confirmButtonText: 'OK',
        timer: type === 'success' ? 3000 : undefined,
        timerProgressBar: type === 'success'
    };
    
    Swal.fire(config);
}

function addLog(message, type = 'info') {
    const logsContainer = document.getElementById('activity-logs');
    const timestamp = new Date().toLocaleTimeString();
    const logClass = type === 'success' ? 'text-success' : 
                    type === 'error' ? 'text-danger' : 
                    type === 'warning' ? 'text-warning' : 'text-info';
    
    const logEntry = document.createElement('div');
    logEntry.className = logClass;
    logEntry.innerHTML = `[${timestamp}] [${type.toUpperCase()}] ${message}`;
    
    logsContainer.appendChild(logEntry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

function clearLogs() {
    const logsContainer = document.getElementById('activity-logs');
    logsContainer.innerHTML = '<div class="text-success">[INFO] Logs cleared</div>';
    addLog('Activity logs cleared', 'info');
}

function handleEmailServiceChange() {
    const emailService = document.getElementById('email-service').value;
    const serviceInfo = document.getElementById('service-info');
    const gmailHelp = document.getElementById('gmail-help');
    
    if (emailService === 'gmail') {
        serviceInfo.innerHTML = '<i class="fas fa-check-circle text-success me-1"></i>Gmail SMTP - Emails will be delivered to real addresses';
        serviceInfo.className = 'form-text text-success';
        if (gmailHelp) gmailHelp.style.display = 'block';
    } else if (emailService === 'mailtrap') {
        serviceInfo.innerHTML = '<i class="fas fa-exclamation-triangle text-warning me-1"></i>Mailtrap - Emails will NOT reach real addresses (Testing only)';
        serviceInfo.className = 'form-text text-warning';
        if (gmailHelp) gmailHelp.style.display = 'none';
    }
    
    addLog(`Email service changed to: ${emailService.toUpperCase()}`, 'info');
}

function testGmailConnection() {
    addLog('Testing Gmail SMTP connection...', 'info');
    
    fetch('/test_gmail_connection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addLog('✅ Gmail connection test successful!', 'success');
            showAlert('Gmail connection successful!', 'success');
        } else {
            addLog(`❌ Gmail connection failed: ${data.message}`, 'error');
            showAlert('Gmail connection failed: ' + data.message, 'error');
        }
    })
    .catch(error => {
        addLog('Gmail connection test error: ' + error.message, 'error');
        showAlert('Gmail connection test failed: ' + error.message, 'error');
    });
}
