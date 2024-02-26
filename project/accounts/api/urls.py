from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('auth/sign-up/',SignUpView.as_view()),
    path('auth/log-in/', UserLoginApiView.as_view()),
    path('auth/log-out/', LogoutAPIView.as_view()),
    path('auth/get-code-reset-password/', GetCodeResetPassword.as_view()),
    path('auth/veryfiy-account/<str:user_id>/', VerifyAccount.as_view()),
    path('auth/verify-code-to-reset-password/<str:user_id>/', VerifyCodeToChangePassword.as_view()),
    path('auth/reset-password/<str:user_id>/', ResetPasswordView.as_view()),
    path('setting/list-info-user/<str:pk>/', ListInformationUserView.as_view()),
    path('setting/update-image/<str:user_id>/',UpdateImageUserView.as_view()),
]