from django.urls import path
from . import views

urlpatterns = [
    path('send-otp/<int:work_id>/', views.send_otp_view, name='send_otp'),
    path('validate-otp/<int:work_id>/', views.validate_otp_view, name='validate_otp'),  # ✅ name must match
]
