from .models import OtpToken,User
from django.core.mail import send_mail
from django.utils import timezone


def generate_and_send_otp(user):
    otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=1))
    message = f"""
        Hi {user.username}, here is your OTP {otp.otp_code}
        It expires in 5 minutes, use the URL below to redirect back to the website
        https://library-api-t70g.onrender.com/verify-email/{user.username}
    """
    try:
        send_mail(
            subject="Email Verification",
            message=message,
            from_email="aliotptest@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        return otp
    except Exception as e:
        otp.delete()
        raise e

