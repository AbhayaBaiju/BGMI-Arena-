from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path("player-dashboard/",views.player_dashboard,name="player_dashboard"),
    path("playerprofile/",views.player_profile,name="player_profile"),
    path("edit-profile/",views.edit_profile,name="edit_profile"),
    path("change-password/",views.change_password,name="change_password"),
    path("view-tournament/",views.view_tournament,name="view_tournament"),
    path("tournament-details/<int:tournament_id>/",views.tournament_details,name="tournament_details"),
    path("booking/<int:tournament_id>/",views.booking,name="booking"),
    path("payment/<int:tournament_id>/",views.payment,name="payment"),
    path("payment-success/<int:tournament_id>/",views.payment_success,name="payment_success"),


]