from django.urls import path
from .views import register_user, login_user, logout_user, get_users, delete_user

urlpatterns = [
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('get_users', get_users, name='get_users'),
    path('delete_user', delete_user, name='delete_user'),
]
