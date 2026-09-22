
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from decimal import Decimal, InvalidOperation
import uuid

from Guest.models import ClanRegistration
from .models import Tournament, Booking


# ============================================================
# CLAN DASHBOARD
# ============================================================

def clan_dashboard(request):

    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)
    except ClanRegistration.DoesNotExist:
        request.session.flush()
        return redirect("login")

    return render(
        request,
        "Clan/clan_dashboard.html",
        {
            "clan": clan
        }
    )


# ============================================================
# CLAN PROFILE
# ============================================================

# def clan_profile(request):

#     if request.session.get("user_type") != "clan":
#         return redirect("login")

#     clan_id = request.session.get("clan_id")

#     if not clan_id:
#         return redirect("login")

#     try:
#         clan = ClanRegistration.objects.get(id=clan_id)
#     except ClanRegistration.DoesNotExist:
#         request.session.flush()
#         return redirect("login")

#     return render(
#         request,
#         "Clan/clan_profile.html",
#         {
#             "clan": clan
#         }
#     )


import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import ClanRegistration


def clan_profile(request):

    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)
    except ClanRegistration.DoesNotExist:
        request.session.flush()
        return redirect("login")

    print("================================")
    print("IMAGE FIELD :", clan.clan_logo)
    print("IMAGE URL   :", clan.clan_logo.url if clan.clan_logo else "NO IMAGE")
    print("MEDIA_ROOT  :", settings.MEDIA_ROOT)

    if clan.clan_logo:
        print("IMAGE PATH  :", clan.clan_logo.path)
        print("FILE EXISTS :", os.path.exists(clan.clan_logo.path))

    print("================================")

    return render(
        request,
        "Clan/clan_profile.html",
        {
            "clan": clan
        }
    )

# ============================================================
# EDIT PROFILE
# ============================================================

def edit_profile(request):

    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    clan = get_object_or_404(
        ClanRegistration,
        id=clan_id
    )

    if request.method == "POST":

        clan.clan_name = request.POST.get(
            "clan_name",
            clan.clan_name
        )

        clan.clan_tag = request.POST.get(
            "clan_tag",
            clan.clan_tag
        )

        clan.captain_name = request.POST.get(
            "captain_name",
            clan.captain_name
        )

        clan.captain_bgmi_id = request.POST.get(
            "captain_bgmi_id",
            clan.captain_bgmi_id
        )

        clan.email = request.POST.get(
            "email",
            clan.email
        )

        clan.phone = request.POST.get(
            "phone",
            clan.phone
        )

        clan.clan_type = request.POST.get(
            "clan_type",
            clan.clan_type
        )

        clan.game_mode = request.POST.get(
            "game_mode",
            clan.game_mode
        )

        if hasattr(clan, "member_count"):

            member_count = request.POST.get("member_count")

            if member_count:
                clan.member_count = member_count

        if hasattr(clan, "location"):

            clan.location = request.POST.get(
                "location",
                clan.location
            )

        if hasattr(clan, "description"):

            clan.description = request.POST.get(
                "description",
                clan.description
            )

        if "clan_logo" in request.FILES:

            clan.clan_logo = request.FILES["clan_logo"]

        try:

            clan.save()

            messages.success(
                request,
                "Clan profile updated successfully!"
            )

            return redirect("clan_profile")

        except Exception as e:

            messages.error(
                request,
                f"Unable to update profile: {e}"
            )

    return render(
        request,
        "Clan/editprofile.html",
        {
            "clan": clan
        }
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

def change_password(request):

    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)

    except ClanRegistration.DoesNotExist:

        request.session.flush()
        return redirect("login")

    if request.method == "POST":

        current_password = request.POST.get(
            "current_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if current_password != clan.password:

            messages.error(
                request,
                "Current password is incorrect."
            )

            return render(
                request,
                "Clan/changepassword.html",
                {"clan": clan}
            )

        if not new_password:

            messages.error(
                request,
                "New password is required."
            )

            return render(
                request,
                "Clan/changepassword.html",
                {"clan": clan}
            )

        if len(new_password) < 6:

            messages.error(
                request,
                "New password must contain at least 6 characters."
            )

            return render(
                request,
                "Clan/changepassword.html",
                {"clan": clan}
            )

        if new_password != confirm_password:

            messages.error(
                request,
                "New password and confirm password do not match."
            )

            return render(
                request,
                "Clan/changepassword.html",
                {"clan": clan}
            )

        if current_password == new_password:

            messages.error(
                request,
                "New password must be different from current password."
            )

            return render(
                request,
                "Clan/changepassword.html",
                {"clan": clan}
            )

        clan.password = new_password
        clan.save()

        messages.success(
            request,
            "Clan password changed successfully!"
        )

        return redirect("clan_profile")

    return render(
        request,
        "Clan/changepassword.html",
        {
            "clan": clan
        }
    )


# ============================================================
# VIEW TOURNAMENTS
# ============================================================

def view_tournaments(request):

    # Check clan login
    if request.session.get("user_type") != "clan":
        return redirect("login")

    # Get logged-in clan ID
    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    # Get clan
    try:
        clan = ClanRegistration.objects.get(id=clan_id)

    except ClanRegistration.DoesNotExist:
        request.session.flush()
        return redirect("login")

    # Get tournaments created by this clan
    tournaments = Tournament.objects.filter(
        clan_id=clan.id
    ).order_by("-created_at")

    return render(
        request,
        "Clan/view_tournaments.html",
        {
            "clan": clan,
            "tournaments": tournaments
        }
    )


# ============================================================
# TOURNAMENT DETAILS
# ============================================================

def tournament_details(request, tournament_id):

    # Check clan login
    if request.session.get("user_type") != "clan":
        return redirect("login")

    # Get clan ID
    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    # Get tournament
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    # Optional security:
    # Make sure the tournament belongs to the logged-in clan
    if tournament.clan_id != int(clan_id):
        return redirect("view_tournaments")

    return render(
        request,
        "Clan/tournament_details.html",
        {
            "tournament": tournament
        }
    )


# ============================================================
# ADD TOURNAMENT
# ============================================================

def add_tournament(request):

    # Check clan login
    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)
    except ClanRegistration.DoesNotExist:
        return redirect("login")

    if request.method == "POST":

        tournament_name = request.POST.get("tournament_name")
        map_name = request.POST.get("map")
        game_mode = request.POST.get("game_mode")

        tournament_date = request.POST.get("tournament_date")
        tournament_time = request.POST.get("tournament_time")

        entry_fee = request.POST.get("entry_fee")
        prize_pool = request.POST.get("prize_pool")

        first_prize = request.POST.get("first_prize")
        second_prize = request.POST.get("second_prize")
        third_prize = request.POST.get("third_prize")

        # IMPORTANT
        total_slot = request.POST.get("total_slot")
        matches = request.POST.get("matches")

        description = request.POST.get("description")

        # Convert Decimal values
        try:
            entry_fee = Decimal(entry_fee or "0")
            prize_pool = Decimal(prize_pool or "0")

            first_prize = Decimal(first_prize or "0")
            second_prize = Decimal(second_prize or "0")
            third_prize = Decimal(third_prize or "0")

        except InvalidOperation:
            messages.error(request, "Please enter valid prize/fee values.")
            return redirect("add_tournament")

        # Convert integer values
        total_slot = int(total_slot or 1)
        matches = int(matches or 1)

        # Create tournament
        Tournament.objects.create(
            clan=clan,

            tournament_name=tournament_name,
            map=map_name,
            game_mode=game_mode,

            tournament_date=tournament_date,
            tournament_time=tournament_time,

            entry_fee=entry_fee,
            prize_pool=prize_pool,

            first_prize=first_prize,
            second_prize=second_prize,
            third_prize=third_prize,

            total_slot=total_slot,
            matches=matches,

            description=description
        )

        messages.success(
            request,
            "Tournament created successfully!"
        )

        return redirect("view_tournaments")

    return render(
        request,
        "Clan/add_tournaments.html"
    )

# ============================================================
# VIEW BOOKINGS
# ============================================================

def view_booking(request):

    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)

    except ClanRegistration.DoesNotExist:
        request.session.flush()
        return redirect("login")

    # ========================================================
    # POST - SAVE GAME ROOM DETAILS
    # ========================================================

    if request.method == "POST":

        tournament_id = request.POST.get(
            "tournament_id",
            ""
        ).strip()

        game_id = request.POST.get(
            "game_id",
            ""
        ).strip()

        game_password = request.POST.get(
            "game_password",
            ""
        ).strip()

        if not tournament_id:
            messages.error(
                request,
                "Please select a tournament."
            )
            return redirect("view_booking")

        if not game_id:
            messages.error(
                request,
                "Game ID is required."
            )
            return redirect("view_booking")

        if not game_password:
            messages.error(
                request,
                "Game password is required."
            )
            return redirect("view_booking")

        try:
            tournament_id = int(tournament_id)

        except (ValueError, TypeError):
            messages.error(
                request,
                "Invalid tournament selected."
            )
            return redirect("view_booking")

        # Check tournament belongs to this clan
        tournament = Tournament.objects.filter(
            id=tournament_id,
            clan_id=clan.id
        ).first()

        if not tournament:
            messages.error(
                request,
                "Tournament not found."
            )
            return redirect("view_booking")

        # Save room details
        Tournament.objects.filter(
            id=tournament_id,
            clan_id=clan.id
        ).update(
            game_id=game_id,
            game_password=game_password
        )

        messages.success(
            request,
            "Room details saved successfully!"
        )

        return redirect(
            "send_whatsapp",
            tournament_id=tournament_id
        )

    # ========================================================
    # GET - TOURNAMENT LIST
    # ========================================================

    tournaments = Tournament.objects.filter(
        clan_id=clan.id
    ).only(
        "id",
        "tournament_name"
    ).order_by("-id")

    # ========================================================
    # GET BOOKINGS
    # ========================================================

    bookings = Booking.objects.filter(
        tournament__clan_id=clan.id
    ).select_related(
        "tournament"
    ).only(
        "id",
        "player_name",
        "bgmi_id",
        "in_game_name",
        "phone",
        "game_mode",
        "slot_number",
        "status",
        "booked_at",
        "tournament__id",
        "tournament__tournament_name"
    ).order_by("-id")

    context = {
        "clan": clan,
        "tournaments": tournaments,
        "bookings": bookings,
        "total_bookings": bookings.count()
    }

    return render(
        request,
        "Clan/view_booking.html",
        context
    )


# ============================================================
# SEND WHATSAPP
# ============================================================

def send_whatsapp(request, tournament_id):

    if request.session.get("user_type") != "clan":
        return redirect("login")

    clan_id = request.session.get("clan_id")

    if not clan_id:
        return redirect("login")

    clan = get_object_or_404(
        ClanRegistration,
        id=clan_id
    )

    try:
        tournament_id = int(tournament_id)

    except (ValueError, TypeError):
        messages.error(
            request,
            "Invalid tournament."
        )
        return redirect("view_booking")

    tournament = Tournament.objects.filter(
        id=tournament_id,
        clan_id=clan.id
    ).first()

    if not tournament:
        messages.error(
            request,
            "Tournament not found."
        )
        return redirect("view_booking")

    bookings = Booking.objects.filter(
        tournament_id=tournament_id
    ).only(
        "id",
        "player_name",
        "phone",
        "slot_number"
    ).order_by(
        "slot_number",
        "id"
    )

    whatsapp_data = []

    for booking in bookings:

        whatsapp_data.append({
            "player_name": booking.player_name,
            "phone": booking.phone
        })

    context = {
        "clan": clan,
        "tournament": tournament,
        "whatsapp_data": whatsapp_data,
        "total_players": len(whatsapp_data)
    }

    return render(
        request,
        "Clan/send_whatsapp.html",
        context
    )




def clan_logout(request):

    request.session.flush()

    messages.success(
        request,
        "Clan logged out successfully."
    )

    return redirect("login")
