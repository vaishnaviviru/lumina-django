# clac/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth views
    path('register/', views.register, name='register'),

    # Developer views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('showcase/add/', views.add_showcase, name='add_showcase'),
    path('showcase/<int:id>/', views.showcase_detail, name='showcase_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # MODERATOR views (rename from 'admin/')
    path('moderation/review/', views.review_queue, name='review_queue'),
    path('moderation/review/<int:id>/approve/', views.approve_showcase, name='approve_showcase'),
    path('moderation/review/<int:id>/reject/', views.reject_showcase, name='reject_showcase'),
     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
