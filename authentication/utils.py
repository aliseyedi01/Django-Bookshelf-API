from .models import OtpToken,User
from django.core.mail import send_mail
from django.utils import timezone


def generate_and_send_otp(user):
    username = user['username']
    email = user['email']
    otp = OtpToken.objects.create(username=username, expires_at=timezone.now() + timezone.timedelta(minutes=1))
    message = f"""
        Hi {username}, here is your OTP {otp.otp_code}
        It expires in 5 minutes, use the URL below to redirect back to the website
        https://library-api-t70g.onrender.com/verify-email/{username}
    """
    try:
        send_mail(
            subject="Email Verification",
            message=message,
            from_email="aliotptest@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return otp
    except Exception as e:
        otp.delete()
        raise e

