from django.urls import path, include
from .views import SignUpView , SignInView, SignOutView , VerifyEmailView , ResendOtpView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("verify-email/<slug:username>", VerifyEmailView.as_view() , name="verify-email"),
    path("resend-otp/", ResendOtpView.as_view(), name="resend-otp"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
]
