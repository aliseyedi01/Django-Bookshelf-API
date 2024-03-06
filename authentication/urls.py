from django.urls import path, include , re_path
from .views import ( SignUpView , SignInView, SignOutView , VerifyEmailView ,
ResendOtpView , MyTokenRefreshView , MyTokenVerifyView)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("verify-email/", VerifyEmailView.as_view() , name="verify-email"),
    path("resend-otp/", ResendOtpView.as_view(), name="resend-otp"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
]
