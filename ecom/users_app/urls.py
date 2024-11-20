from django.urls import path
from .views import LoginAPIView, ResetPasswordView, ValidateOTPView, CreateUserView, UpdateUserView, CheckEmailView, ResetPasswordRequestAPIView
from knox import views as knox_views
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    path('update_user/<pk>/', UpdateUserView.as_view(), name='update-user'),
    path('check_email/', CheckEmailView.as_view(), name='check-email'),
    path('forget_password/', ResetPasswordRequestAPIView.as_view(), name='forget-password'),
    path('forgot_password/validate_otp/', ValidateOTPView.as_view(), name='validate-otp'),
    path('reset/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
]