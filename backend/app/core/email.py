import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailUtils:
    @staticmethod
    def send_password_reset_email(email: str, reset_token: str) -> bool:
        try:
            reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset Request"
            message["From"] = settings.FROM_EMAIL
            message["To"] = email

            html = f"""
            <html>
              <body>
                <h2>Password Reset</h2>
                <p><a href="{reset_link}">Reset your password</a></p>
                <p>Link expires in 24 hours.</p>
              </body>
            </html>
            """
            message.attach(MIMEText(html, "html"))

            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.FROM_EMAIL, email, message.as_string())
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

    @staticmethod
    def send_welcome_email(email: str, name: str) -> bool:
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Welcome!"
            message["From"] = settings.FROM_EMAIL
            message["To"] = email

            html = f"""
            <html>
              <body>
                <h2>Welcome, {name}!</h2>
                <p>Your account is ready to use.</p>
              </body>
            </html>
            """
            message.attach(MIMEText(html, "html"))

            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.FROM_EMAIL, email, message.as_string())
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
