from django.urls import path
from .views import home_page, login_page, register_page, get_categories, create_post, get_posts, management_page, \
    get_stats, edit_post,delete_post,create_review,get_reviews,profile_page, add_to_favorite, edit_profile,about_us_page,change_password,get_status

urlpatterns = [
    path('', home_page, name='home_page'),
    path('login', login_page, name='login_page'),
    path('register', register_page, name='register_page'),
    path('management', management_page, name='management_page'),
    path('get_categories', get_categories, name='get_categories'),
    path('get_status', get_status, name='get_status'),
    path('get_posts', get_posts, name='get_posts'),
    path('create_post', create_post, name='create_post'),
    path('get_stats', get_stats, name='get_stats'),
    path('edit_post/<int:pk>', edit_post, name='edit_post'),
    path('delete_post/<int:pk>', delete_post, name='delete_post'),
    path('create_review', create_review, name='create_review'),
    path('get_reviews', get_reviews, name='get_reviews'),
    path('profile', profile_page, name='profile_page'),
    path('add_to_favorite', add_to_favorite, name='add_to_favorite'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('about_us', about_us_page, name='about_us_page'),
    path('change_password', change_password, name='change_password'),
 

]
