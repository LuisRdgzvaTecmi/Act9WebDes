import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_email(to, subject, body_html):
    """Send an email using smtplib with credentials from .env"""
    host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    port = int(os.getenv('EMAIL_PORT', '465'))
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')

    if not user or not password:
        print('[MAIL] EMAIL_USER or EMAIL_PASS not set — skipping email.')
        return False

    msg = MIMEMultipart('alternative')
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body_html, 'html'))

    try:
        if port == 465:
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(user, password)
                server.sendmail(user, to, msg.as_string())
        else:
            with smtplib.SMTP(host, port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(user, password)
                server.sendmail(user, to, msg.as_string())
        print(f'[MAIL] Sent "{subject}" to {to}')
        return True
    except Exception as e:
        print(f'[MAIL] Failed to send email: {e}')
        return False


def send_welcome_email(username, email):
    """Send a welcome email after successful registration."""
    subject = 'Welcome to the Act9 HW8 App!'
    body = f"""
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; background: #0a0e17; color: #f1f5f9; padding: 2rem;">
        <div style="max-width: 500px; margin: 0 auto; background: #1a1f2e; border-radius: 12px; padding: 2rem; border: 1px solid rgba(99,102,241,0.15);">
            <h1 style="color: #a78bfa; margin-top: 0;">Welcome, {username}!</h1>
            <p>Your account has been successfully created on <strong>Activity 9 Dashboard</strong>.</p>
            <p>You can now log in and access your personal dashboard.</p>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0;">
            <p style="color: #64748b; font-size: 0.85rem;">Homework 8 — Custom automated mail notifications</p>
        </div>
    </body>
    </html>
    """
    return send_email(email, subject, body)


def send_login_alert_email(username, email):
    """Send a login alert email when a user signs in."""
    now = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    subject = 'Login Alert —  Act9 HW8 App'
    body = f"""
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; background: #0a0e17; color: #f1f5f9; padding: 2rem;">
        <div style="max-width: 500px; margin: 0 auto; background: #1a1f2e; border-radius: 12px; padding: 2rem; border: 1px solid rgba(99,102,241,0.15);">
            <h1 style="color: #a78bfa; margin-top: 0;">Login Detected</h1>
            <p>Hello <strong>{username}</strong>, a login to your account was detected.</p>
            <p><strong>Date:</strong> {now}</p>
            <p>If this was not you, please secure your account immediately.</p>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0;">
            <p style="color: #64748b; font-size: 0.85rem;">Homework 8 — Custom automated mail notifications</p>
        </div>
    </body>
    </html>
    """
    return send_email(email, subject, body)
