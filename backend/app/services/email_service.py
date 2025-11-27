"""Email service for sending OTP codes via Gmail SMTP."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger

from app.config import settings


def send_otp_email(to_email: str, otp_code: str) -> bool:
    """
    Send OTP code to user's email via Gmail SMTP.

    Args:
        to_email: Recipient email address
        otp_code: 6-digit OTP code

    Returns:
        True if email sent successfully, False otherwise
    """
    if not settings.smtp_email or not settings.smtp_password:
        logger.error("SMTP credentials not configured")
        return False

    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your Netra Login Code"
        msg["From"] = f"Netra <{settings.smtp_email}>"
        msg["To"] = to_email

        # Plain text version
        text = f"""
Your Netra verification code is: {otp_code}

This code will expire in {settings.otp_expiry_minutes} minutes.

If you didn't request this code, please ignore this email.

- Netra AI
"""

        # HTML version
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #191022; color: #e5e5e5; padding: 20px; }}
        .container {{ max-width: 400px; margin: 0 auto; background: linear-gradient(135deg, #2d1f3d 0%, #1a1225 100%); border-radius: 16px; padding: 40px; text-align: center; }}
        .logo {{ font-size: 32px; font-weight: bold; color: #a855f7; margin-bottom: 20px; }}
        .code {{ font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #ffffff; background: rgba(168, 85, 247, 0.2); padding: 20px 30px; border-radius: 12px; margin: 20px 0; border: 1px solid rgba(168, 85, 247, 0.3); }}
        .expiry {{ color: #9ca3af; font-size: 14px; margin-top: 20px; }}
        .footer {{ color: #6b7280; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Netra</div>
        <p>Your verification code is:</p>
        <div class="code">{otp_code}</div>
        <p class="expiry">This code expires in {settings.otp_expiry_minutes} minutes</p>
        <p class="footer">If you didn't request this code, please ignore this email.</p>
    </div>
</body>
</html>
"""

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Connect to Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.smtp_email, settings.smtp_password)
            server.sendmail(settings.smtp_email, to_email, msg.as_string())

        logger.info(f"OTP email sent to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail SMTP authentication failed. Check your App Password.")
        return False
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")
        return False
