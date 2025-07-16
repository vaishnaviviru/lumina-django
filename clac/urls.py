from django.contrib.auth import views as auth_views
from django.urls import path,include
from clac.views import home
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', home, name='home'),
    path("login/", auth_views.LoginView.as_view(template_name="clac/login.html"), name="login"),
    # or use LoginView.as_view()


    # Auth views
    path("register/", views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    # Developer views
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("showcase/add/", views.add_showcase, name="add_showcase"),
    path("showcase/<int:id>/", views.showcase_detail, name="showcase_detail"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("ranking/", views.ranking_view, name="ranking"),
    # Moderator views
    path("moderation/", views.moderation_dashboard, name="moderation_dashboard"),
    path("moderation/review/", views.review_queue, name="review_queue"),
     path("accounts/", include("django.contrib.auth.urls")),
    path(
        "moderation/review/<int:id>/approve/",
        views.approve_showcase,
        name="approve_showcase",
    ),
    path(
        "moderation/review/<int:id>/reject/",
        views.reject_showcase,
        name="reject_showcase",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)