from .models import OtpToken, User
from django.core.mail import send_mail
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse


def generate_and_send_otp(user):
    username = user['username']
    first_name = user['first_name']
    email = user['email']
    otp = OtpToken.objects.create(username=username, expires_at=timezone.now() +
                                  timezone.timedelta(seconds=90))
    message = f"""
        Hi {first_name} 🖐️
        Here is your One-Time Password (OTP) : {otp.otp_code}
        It expires in 90 seconds
        Please use this OTP to verify your Email
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


class SwaggerResponse:
    UNAUTHORIZED = OpenApiResponse(description="Unauthorized")
    FORBIDDEN = OpenApiResponse(description="Forbidden")
    NOT_FOUND = OpenApiResponse(description="Not Found")
    SUCCESS = OpenApiResponse(description="Success")
    BAD_REQUEST = OpenApiResponse(description="Bad Request")
    INTERNAL_SERVER_ERROR = OpenApiResponse(description="Internal Server Error")
    CREATED = OpenApiResponse(description="Created")
    NO_CONTENT = OpenApiResponse(description="No Content")
