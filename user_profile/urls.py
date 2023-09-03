from django.urls import path, include

from user_profile.views import login_user
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('oauth/', include('social_django.urls', namespace='social')),

    path('register_user/', register_user, name='register_user'),
   # path('registration/', registration, name='registration'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('profile/', profile, name='profile'),
    path('change_profile_picture/', change_profile_picture, name='change_profile_picture'),
    path('view_user_information/<str:username>/', view_user_information, name="view_user_information"),
    path('follow_or_unfollow/<int:user_id>/', follow_or_unfollow_user, name='follow_or_unfollow_user'),
    path('user_notifications/', user_notifications, name='user_notifications'),
    path('mute_or_unmute_user/<int:user_id>/', mute_or_unmute_user, name='mute_or_unmute_user'),



    path('reset/password/',PasswordResetView.as_view(template_name='reset_pass.html'),name="password_reset"),
    path('reset/password/done',PasswordResetDoneView.as_view(template_name='reset_pass_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset/done/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
    
]