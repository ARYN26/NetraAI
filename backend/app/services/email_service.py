"""Email service for sending OTP codes via Gmail SMTP."""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from app.config import settings

# Thread pool for non-blocking email sending
_email_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="email_worker")

# SMTP connection timeout (seconds)
SMTP_TIMEOUT = 30


def _send_email_sync(to_email: str, msg: MIMEMultipart) -> bool:
    """
    Synchronous email sending (runs in thread pool).

    Args:
        to_email: Recipient email address
        msg: Prepared email message

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create SSL context for secure connection
        context = ssl.create_default_context()

        # Connect to Gmail SMTP with timeout
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context, timeout=SMTP_TIMEOUT
        ) as server:
            server.login(settings.smtp_email, settings.smtp_password)
            server.sendmail(settings.smtp_email, to_email, msg.as_string())

        logger.info(f"OTP email sent to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail SMTP authentication failed. Check your App Password.")
        return False
    except TimeoutError:
        logger.error(f"SMTP connection timed out for {to_email}")
        return False
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")
        return False


def send_otp_email(to_email: str, otp_code: str) -> bool:
    """
    Send OTP code to user's email via Gmail SMTP.

    Uses a thread pool to avoid blocking the async event loop.

    Args:
        to_email: Recipient email address
        otp_code: 6-digit OTP code

    Returns:
        True if email was queued successfully (actual send is async)
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

        # Submit to thread pool (non-blocking)
        future = _email_executor.submit(_send_email_sync, to_email, msg)

        # Wait for result with timeout (to detect immediate failures)
        # For truly async, you could return True immediately and log failures
        result = future.result(timeout=SMTP_TIMEOUT + 5)
        return result

    except Exception as e:
        logger.error(f"Failed to queue OTP email: {e}")
        return False
