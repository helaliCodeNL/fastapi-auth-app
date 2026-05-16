import pyotp
import qrcode
from io import BytesIO
import base64
from app.core.config import settings

class TwoFAUtils:
    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()

    @staticmethod
    def verify_token(secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)

    @staticmethod
    def generate_qr_code(email: str, secret: str) -> str:
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=email, issuer_name=settings.PROJECT_NAME)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
