from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('admin_login/', AdminLoginView.as_view(), name='admin_login'),

    path('verify_email/', VerifyEmailView.as_view(), name='verify_email'),
    path('send_otp/', SendOtpView.as_view(), name='send_otp'),


    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/', CustomerView.as_view(), name='user_list'),
    path('user/<int:pk>/', CustomerView.as_view(), name='user_detail'),



    path('add_new_location/', LocationView.as_view(), name='add_new_location'),
    path('all_location/', LocationView.as_view(), name='all_location'),
    path('update_location/<int:pk>/', LocationView.as_view(), name='update_location'),
    path('delete_location/<int:pk>/', LocationView.as_view(), name='delete_location'),
    path('location/<int:pk>/', LocationView.as_view(), name='location_detail'),

]