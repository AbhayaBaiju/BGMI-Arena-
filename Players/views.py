from django.shortcuts import render,redirect
from Guest.models import PlayerRegistration
from Guest.models import ClanRegistration
from Clan.models import Tournament,Booking
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Max



# Create your views here.
def player_dashboard(request):

    # Check player login
    if request.session.get("user_type") != "player":
        return redirect("login")

    player_id = request.session.get("player_id")

    if not player_id:
        return redirect("login")

    try:
        player = PlayerRegistration.objects.get(id=player_id)

    except PlayerRegistration.DoesNotExist:
        request.session.flush()
        return redirect("login")

    # Get all registered clans
    clans = ClanRegistration.objects.all().order_by("-id")

    return render(
        request,
        "Players/player_dashboard.html",
        {
            "player": player,
            "clans": clans
        }
    )

def player_profile(request):

    if request.session.get("user_type") != "player":
        return redirect("login")

    player_id = request.session.get("player_id")

    if not player_id:
        return redirect("login")

    try:
        player = PlayerRegistration.objects.get(id=player_id)

    except PlayerRegistration.DoesNotExist:
        request.session.flush()
        return redirect("login")

    return render(
        request,
        "Players/player_profile.html",
        {
            "player": player
        }
    )


# def edit_profile(request):

#     # Check player login
#     if request.session.get("user_type") != "player":
#         return redirect("login")

#     player_id = request.session.get("player_id")

#     if not player_id:
#         return redirect("login")

#     try:
#         player = PlayerRegistration.objects.get(id=player_id)

#     except PlayerRegistration.DoesNotExist:
#         request.session.flush()
#         return redirect("login")

#     if request.method == "POST":

#         full_name = request.POST.get("full_name", "").strip()
#         username = request.POST.get("username", "").strip()
#         email = request.POST.get("email", "").strip()
#         phone = request.POST.get("phone", "").strip()
#         bgmi_id = request.POST.get("bgmi_id", "").strip()
#         in_game_name = request.POST.get("in_game_name", "").strip()
#         game_mode = request.POST.get("game_mode")
#         player_role = request.POST.get("player_role")

#         if not full_name:
#             messages.error(request, "Full name is required.")
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         if not username:
#             messages.error(request, "Username is required.")
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         if not email:
#             messages.error(request, "Email is required.")
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         if not phone.isdigit() or len(phone) != 10:
#             messages.error(
#                 request,
#                 "Phone number must contain exactly 10 digits."
#             )
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         # Username duplicate check
#         if PlayerRegistration.objects.filter(
#             username=username
#         ).exclude(id=player.id).exists():

#             messages.error(request, "Username already exists.")
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         # Email duplicate check
#         if PlayerRegistration.objects.filter(
#             email=email
#         ).exclude(id=player.id).exists():

#             messages.error(request, "Email already exists.")
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         # BGMI ID duplicate check
#         if PlayerRegistration.objects.filter(
#             bgmi_id=bgmi_id
#         ).exclude(id=player.id).exists():

#             messages.error(request, "BGMI ID already exists.")
#             return render(request, "Players/editprofile.html",
#                           {"player": player})

#         # Update player
#         player.full_name = full_name
#         player.username = username
#         player.email = email
#         player.phone = phone
#         player.bgmi_id = bgmi_id
#         player.in_game_name = in_game_name
#         player.game_mode = game_mode
#         player.player_role = player_role

#         if request.FILES.get("profile_image"):
#             player.profile_image = request.FILES.get("profile_image")

#         player.save()

#         messages.success(
#             request,
#             "Profile updated successfully!"
#         )

#         return redirect("player_profile")

#     return render(
#         request,
#         "Players/editprofile.html",
#         {
#             "player": player
#         }
#     )

# def change_password(request):


#     if request.session.get("user_type") != "player":
#         return redirect("login")

#     player_id = request.session.get("player_id")

#     if not player_id:
#         return redirect("login")


#     try:
#         player = PlayerRegistration.objects.get(
#             id=player_id
#         )

#     except PlayerRegistration.DoesNotExist:

#         request.session.flush()

#         return redirect("login")


#     if request.method == "POST":

#         current_password = request.POST.get(
#             "current_password"
#         )

#         new_password = request.POST.get(
#             "new_password"
#         )

#         confirm_password = request.POST.get(
#             "confirm_password"
#         )


#         if current_password != player.password:

#             messages.error(
#                 request,
#                 "Current password is incorrect."
#             )

#             return render(
#                 request,
#                 "Players/changepassword.html",
#                 {"player": player}
#             )


#         if not new_password:

#             messages.error(
#                 request,
#                 "New password is required."
#             )

#             return render(
#                 request,
#                 "Players/changepassword.html",
#                 {"player": player}
#             )


#         if len(new_password) < 6:

#             messages.error(
#                 request,
#                 "New password must contain at least 6 characters."
#             )

#             return render(
#                 request,
#                 "Players/changepassword.html",
#                 {"player": player}
#             )


#         if new_password != confirm_password:

#             messages.error(
#                 request,
#                 "New password and confirm password do not match."
#             )

#             return render(
#                 request,
#                 "Players/changepassword.html",
#                 {"player": player}
#             )




#         if current_password == new_password:

#             messages.error(
#                 request,
#                 "New password must be different from current password."
#             )

#             return render(
#                 request,
#                 "Players/changepassword.html",
#                 {"player": player}
#             )

#         player.password = new_password

#         player.save()

#         messages.success(
#             request,
#             "Password changed successfully!"
#         )


#         return redirect("player_profile")


#     return render(
#         request,
#         "Players/changepassword.html",
#         {
#             "player": player
#         }
#     )


def get_logged_in_player(request):

    user_type = request.session.get("user_type")
    player_id = request.session.get("player_id")

    print("================================")
    print("USER TYPE:", user_type)
    print("PLAYER ID:", player_id)
    print("SESSION KEY:", request.session.session_key)
    print("ALL SESSION:", dict(request.session))
    print("================================")

    if user_type != "player":
        return None

    if not player_id:
        return None

    try:
        player = PlayerRegistration.objects.get(id=player_id)
        print("PLAYER FOUND:", player.username)
        return player

    except PlayerRegistration.DoesNotExist:
        print("PLAYER NOT FOUND")
        return None

def player_profile(request):

    player = get_logged_in_player(request)

    if not player:
        return redirect("login")

    return render(
        request,
        "Players/player_profile.html",
        {
            "player": player
        }
    )


def edit_profile(request):

    player = get_logged_in_player(request)

    if not player:
        return redirect("login")

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        bgmi_id = request.POST.get("bgmi_id", "").strip()
        in_game_name = request.POST.get("in_game_name", "").strip()
        game_mode = request.POST.get("game_mode")
        player_role = request.POST.get("player_role")

        if not full_name:
            messages.error(request, "Full name is required.")
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        if not username:
            messages.error(request, "Username is required.")
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        if not email:
            messages.error(request, "Email is required.")
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        if not phone.isdigit() or len(phone) != 10:
            messages.error(
                request,
                "Phone number must contain exactly 10 digits."
            )
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        # Username
        if PlayerRegistration.objects.filter(
            username=username
        ).exclude(id=player.id).exists():

            messages.error(request, "Username already exists.")
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        # Email
        if PlayerRegistration.objects.filter(
            email=email
        ).exclude(id=player.id).exists():

            messages.error(request, "Email already exists.")
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        # BGMI ID
        if PlayerRegistration.objects.filter(
            bgmi_id=bgmi_id
        ).exclude(id=player.id).exists():

            messages.error(request, "BGMI ID already exists.")
            return render(
                request,
                "Players/editprofile.html",
                {"player": player}
            )

        # Update
        player.full_name = full_name
        player.username = username
        player.email = email
        player.phone = phone
        player.bgmi_id = bgmi_id
        player.in_game_name = in_game_name
        player.game_mode = game_mode
        player.player_role = player_role

        if request.FILES.get("profile_image"):
            player.profile_image = request.FILES.get("profile_image")

        player.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect("player_profile")

    return render(
        request,
        "Players/editprofile.html",
        {
            "player": player
        }
    )


def change_password(request):

    player = get_logged_in_player(request)

    if not player:
        return redirect("login")

    if request.method == "POST":

        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if current_password != player.password:

            messages.error(
                request,
                "Current password is incorrect."
            )

            return render(
                request,
                "Players/changepassword.html",
                {"player": player}
            )

        if not new_password:

            messages.error(
                request,
                "New password is required."
            )

            return render(
                request,
                "Players/changepassword.html",
                {"player": player}
            )

        if len(new_password) < 6:

            messages.error(
                request,
                "New password must contain at least 6 characters."
            )

            return render(
                request,
                "Players/changepassword.html",
                {"player": player}
            )

        if new_password != confirm_password:

            messages.error(
                request,
                "New password and confirm password do not match."
            )

            return render(
                request,
                "Players/changepassword.html",
                {"player": player}
            )

        if current_password == new_password:

            messages.error(
                request,
                "New password must be different from current password."
            )

            return render(
                request,
                "Players/changepassword.html",
                {"player": player}
            )

        player.password = new_password
        player.save()

        messages.success(
            request,
            "Password changed successfully!"
        )

        return redirect("player_profile")

    return render(
        request,
        "Players/changepassword.html",
        {
            "player": player
        }
    )






def view_tournament(request):

    # Check player login
    if request.session.get("user_type") != "player":
        return redirect("login")

    # Get all tournaments
    tournaments = Tournament.objects.all().order_by("-created_at")

    context = {
        "tournaments": tournaments,
    }

    return render(
        request,
        "Players/view_tournament.html",
        context
    )
def tournament_details(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    return render(
        request,
        "Players/tournament_details.html",
        {
            "tournament": tournament
        }
    )





# ============================================================
# BOOK TOURNAMENT
# ============================================================

def booking(request, tournament_id):

    # Check player login
    if request.session.get("user_type") != "player":
        return redirect("login")

    player_id = request.session.get("player_id")

    if not player_id:
        return redirect("login")

    player = get_object_or_404(
        PlayerRegistration,
        id=player_id
    )

    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    # Check already booked
    already_booked = Booking.objects.filter(
        player=player,
        tournament=tournament
    ).exists()

    if already_booked:

        messages.warning(
            request,
            "You have already booked this tournament."
        )

        return redirect(
            "tournament_details",
            tournament_id=tournament.id
        )

    # Check available slots
    if tournament.total_slot <= 0:

        messages.error(
            request,
            "Sorry! No slots are available."
        )

        return redirect(
            "tournament_details",
            tournament_id=tournament.id
        )

    # Store booking information
    request.session["booking_data"] = {

        "tournament_id": tournament.id,

        "player_id": player.id,

    }

    return redirect(
        "payment",
        tournament_id=tournament.id
    )


# ============================================================
# PAYMENT PAGE
# ============================================================

def payment(request, tournament_id):

    if request.session.get("user_type") != "player":
        return redirect("login")

    player_id = request.session.get("player_id")

    if not player_id:
        return redirect("login")

    player = get_object_or_404(
        PlayerRegistration,
        id=player_id
    )

    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    context = {

        "player": player,

        "tournament": tournament,

    }

    return render(
        request,
        "Players/payment.html",
        context
    )


# ============================================================
# PAYMENT SUCCESS
# ============================================================

def payment_success(request, tournament_id):

    if request.session.get("user_type") != "player":
        return redirect("login")

    player_id = request.session.get("player_id")

    if not player_id:
        return redirect("login")

    player = get_object_or_404(
        PlayerRegistration,
        id=player_id
    )

    # Use transaction so slot allocation is safe
    with transaction.atomic():

        tournament = Tournament.objects.select_for_update().get(
            id=tournament_id
        )

        # ----------------------------------------------------
        # Check already booked
        # ----------------------------------------------------

        already_booked = Booking.objects.filter(
            player=player,
            tournament=tournament
        ).exists()

        if already_booked:

            messages.warning(
                request,
                "You have already booked this tournament."
            )

            return redirect(
                "tournament_details",
                tournament_id=tournament.id
            )

        # ----------------------------------------------------
        # Check slot availability
        # ----------------------------------------------------

        if tournament.total_slot <= 0:

            messages.error(
                request,
                "Sorry! No slots are available."
            )

            return redirect(
                "tournament_details",
                tournament_id=tournament.id
            )

        # ----------------------------------------------------
        # Find last slot number
        # ----------------------------------------------------

        last_slot = Booking.objects.filter(
            tournament=tournament
        ).aggregate(
            Max("slot_number")
        )["slot_number__max"]

        if last_slot is None:
            slot_number = 1
        else:
            slot_number = last_slot + 1

        # ----------------------------------------------------
        # Create booking
        # ----------------------------------------------------

        Booking.objects.create(

            player=player,

            tournament=tournament,

            player_name=player.full_name,

            bgmi_id=player.bgmi_id,

            in_game_name=player.in_game_name,

            phone=player.phone,

            game_mode=player.game_mode,

            slot_number=slot_number,

            status="Booked"

        )

        # ----------------------------------------------------
        # Reduce available slots
        # ----------------------------------------------------

        tournament.total_slot -= 1

        tournament.save(
            update_fields=["total_slot"]
        )

    # Clear temporary booking data
    request.session.pop(
        "booking_data",
        None
    )

    return render(
        request,
        "Players/payment_success.html",
        {
            "tournament": tournament,
            "slot_number": slot_number
        }
    )