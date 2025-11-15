from django.urls import path
from . import views

urlpatterns = [
    path('add-work/', views.add_work_view, name='add_work'),
    path('accept-work/<int:work_id>/', views.accept_work, name='accept_work'),
    path('complete-work/<int:work_id>/', views.complete_work, name='complete_work'),
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
]
