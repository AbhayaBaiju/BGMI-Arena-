from django.urls import path
from . import views


urlpatterns = [

    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        "dashboard/",
        views.clan_dashboard,
        name="clan_dashboard"
    ),

    # ========================================================
    # PROFILE
    # ========================================================

    path(
        "profile/",
        views.clan_profile,
        name="clan_profile"
    ),

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profiles"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_passwords"
    ),

    # ========================================================
    # TOURNAMENTS
    # ========================================================
  path(
        "view-tournaments/",
        views.view_tournaments,
        name="view_tournaments"
    ),

    path(
        "tournament-details/<int:tournament_id>/",
        views.tournament_details,
        name="tournament_detail"
    ),

    path(
        "add-tournament/",
        views.add_tournament,
        name="add_tournament"
    ),

    # ========================================================
    # BOOKINGS
    # ========================================================

    path(
        "view-booking/",
        views.view_booking,
        name="view_booking"
    ),

    # ========================================================
    # WHATSAPP
    # ========================================================

    path(
        "send-whatsapp/<int:tournament_id>/",
        views.send_whatsapp,
        name="send_whatsapp"
    ),


    path(
        "logout/",
        views.clan_logout,
        name="clan_logout"
    ),
]