from django.urls import path, include , re_path
from .views import  SignUpView , SignInView, SignOutView , VerifyEmailView ,ResendOtpView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("otp/check/", VerifyEmailView.as_view() , name="verify-email"),
    path("otp/resend/", ResendOtpView.as_view(), name="resend-otp"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
]