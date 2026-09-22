from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path('register/',views.registration_type,name='registration_type'),
    path('player-register/',views.player_register,name='player_register'),
    path('clan-register/',views.clan_register,name='clan_register'),
    path("login/", views.login, name="login"),
    path('admin-login/', views.admin_login, name='admin_login'),
    path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),

path(
    "player-details/",
    views.player_details,
    name="player_details"
),

path(
    "clans/",
    views.clan_list,
    name="clan_list"
),

path(
    "clan-details/<int:clan_id>/",
    views.clan_details,
    name="clan_details"
),

path(
    "clan-verification/",
    views.clan_verification,
    name="clan_verification"
),

path(
    "verified-clans/",
    views.verified_clans,
    name="verified_clans"
),

path(
    "verify-clan/<int:clan_id>/",
    views.verify_clan,
    name="verify_clan"
),

path(
    "reject-clan/<int:clan_id>/",
    views.reject_clan,
    name="reject_clan"
),
path(
        "admin/clan-verification/<int:clan_id>/unverify/",
        views.unverify_clan,
        name="unverify_clan"
),

path(
    "admin-logout/",
    views.admin_logout,
    name="admin_logout"
),
    path("logout/", views.logout, name="logout"),
]
