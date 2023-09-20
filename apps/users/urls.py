from django.urls import path

from .views import CreateUserView, VerifyAPIView, GetNewVerification, ChangeUserInformationAPIView, \
    ChangeUserPhotoAPIView, LoginAPIView, LoginRefreshAPIView, LogoutAPIView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), ),
    path('login/refresh/', LoginRefreshAPIView.as_view(), ),
    path('logout/', LogoutAPIView.as_view(), ),
    path('signup/', CreateUserView.as_view(), ),
    path('verify/', VerifyAPIView.as_view(), ),
    path('new-verify/', GetNewVerification.as_view(), ),
    path('change-user/', ChangeUserInformationAPIView.as_view(), ),
    path('change-user-photo/', ChangeUserPhotoAPIView.as_view(), ),
    path('forgot-password/', ForgotPasswordView.as_view(), ),
    path('reset-password/', ResetPasswordView.as_view(), ),
]
