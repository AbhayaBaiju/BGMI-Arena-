
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import PlayerRegistration, ClanRegistration
from Clan.models import Tournament


# =========================================================
# HOME / INDEX
# =========================================================

def index(request):

    tournaments = (
        Tournament.objects
        .select_related("clan")
        .order_by("-id")
    )

    return render(
        request,
        "Guest/index.html",
        {
            "tournaments": tournaments
        }
    )


# =========================================================
# REGISTRATION TYPE
# =========================================================

def registration_type(request):
    return render(
        request,
        "Guest/registration_type.html"
    )


# =========================================================
# PLAYER REGISTRATION
# =========================================================

def player_register(request):

    if request.method == "POST":

        # Get form data
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        bgmi_id = request.POST.get("bgmi_id")
        in_game_name = request.POST.get("in_game_name")
        game_mode = request.POST.get("game_mode")
        player_role = request.POST.get("player_role")

        profile_image = request.FILES.get("profile_image")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # -------------------------------------------------
        # Password validation
        # -------------------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Password and Confirm Password do not match."
            )

            return render(
                request,
                "Guest/player_registration.html"
            )

        # -------------------------------------------------
        # Phone validation
        # -------------------------------------------------

        if not phone or not phone.isdigit() or len(phone) != 10:

            messages.error(
                request,
                "Phone number must contain exactly 10 digits."
            )

            return render(
                request,
                "Guest/player_registration.html"
            )

        # -------------------------------------------------
        # Username validation
        # -------------------------------------------------

        if PlayerRegistration.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return render(
                request,
                "Guest/player_registration.html"
            )

        # -------------------------------------------------
        # Email validation
        # -------------------------------------------------

        if PlayerRegistration.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email address is already registered."
            )

            return render(
                request,
                "Guest/player_registration.html"
            )

        # -------------------------------------------------
        # BGMI ID validation
        # -------------------------------------------------

        if PlayerRegistration.objects.filter(
            bgmi_id=bgmi_id
        ).exists():

            messages.error(
                request,
                "This BGMI ID is already registered."
            )

            return render(
                request,
                "Guest/player_registration.html"
            )

        # -------------------------------------------------
        # Save player
        # -------------------------------------------------

        player = PlayerRegistration(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            bgmi_id=bgmi_id,
            in_game_name=in_game_name,
            game_mode=game_mode,
            player_role=player_role,
            profile_image=profile_image,
            password=password
        )

        player.save()

        # -------------------------------------------------
        # Success
        # -------------------------------------------------

        messages.success(
            request,
            "Player registration successful!"
        )

        return redirect("login")

    return render(
        request,
        "Guest/player_registration.html"
    )


# =========================================================
# CLAN REGISTRATION
# =========================================================

def clan_register(request):

    if request.method == "POST":

        # Get form data
        clan_name = request.POST.get("clan_name")
        clan_tag = request.POST.get("clan_tag")
        captain_name = request.POST.get("captain_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        clan_type = request.POST.get("clan_type")

        captain_bgmi_id = request.POST.get("captain_bgmi_id")
        game_mode = request.POST.get("game_mode")
        member_count = request.POST.get("member_count")

        location = request.POST.get("location")
        description = request.POST.get("description")

        clan_logo = request.FILES.get("clan_logo")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # -------------------------------------------------
        # Password validation
        # -------------------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Password and Confirm Password do not match."
            )

            return render(
                request,
                "Guest/clan_registration.html"
            )

        # -------------------------------------------------
        # Phone validation
        # -------------------------------------------------

        if not phone or not phone.isdigit() or len(phone) != 10:

            messages.error(
                request,
                "Phone number must contain exactly 10 digits."
            )

            return render(
                request,
                "Guest/clan_registration.html"
            )

        # -------------------------------------------------
        # Clan Tag validation
        # -------------------------------------------------

        if ClanRegistration.objects.filter(
            clan_tag=clan_tag
        ).exists():

            messages.error(
                request,
                "This Clan Tag is already registered."
            )

            return render(
                request,
                "Guest/clan_registration.html"
            )

        # -------------------------------------------------
        # Email validation
        # -------------------------------------------------

        if ClanRegistration.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email address is already registered."
            )

            return render(
                request,
                "Guest/clan_registration.html"
            )

        # -------------------------------------------------
        # Captain BGMI ID validation
        # -------------------------------------------------

        if ClanRegistration.objects.filter(
            captain_bgmi_id=captain_bgmi_id
        ).exists():

            messages.error(
                request,
                "This Captain BGMI ID is already registered."
            )

            return render(
                request,
                "Guest/clan_registration.html"
            )

        # -------------------------------------------------
        # Save clan
        # -------------------------------------------------

        clan = ClanRegistration(
            clan_name=clan_name,
            clan_tag=clan_tag,
            captain_name=captain_name,
            email=email,
            phone=phone,
            clan_type=clan_type,
            captain_bgmi_id=captain_bgmi_id,
            game_mode=game_mode,
            member_count=member_count,
            location=location,
            description=description,
            clan_logo=clan_logo,
            password=password
        )

        clan.save()

        # -------------------------------------------------
        # Success
        # -------------------------------------------------

        messages.success(
            request,
            "Clan registration successful!"
        )

        return redirect("login")

    return render(
        request,
        "Guest/clan_registration.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login(request):

    if request.method == "POST":

        user_type = request.POST.get("user_type")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ==========================================
        # PLAYER LOGIN
        # ==========================================

        if user_type == "player":

            try:
                player = PlayerRegistration.objects.get(
                    username=username
                )

                if player.password == password:

                    request.session["user_type"] = "player"
                    request.session["player_id"] = player.id

                    return redirect("player_dashboard")

                else:

                    messages.error(
                        request,
                        "Invalid username or password."
                    )

            except PlayerRegistration.DoesNotExist:

                messages.error(
                    request,
                    "Invalid username or password."
                )


        # ==========================================
        # CLAN LOGIN
        # ==========================================

        elif user_type == "clan":

            try:

                clan = ClanRegistration.objects.get(
                    clan_name=username
                )

                # ======================================
                # CHECK PASSWORD
                # ======================================

                if clan.password != password:

                    messages.error(
                        request,
                        "Invalid clan name or password."
                    )

                    return redirect("login")


                # ======================================
                # CHECK ADMIN VERIFICATION
                # ======================================

                if not clan.is_verified:

                    messages.error(
                        request,
                        "Your clan has not been verified by the admin yet."
                    )

                    return redirect("login")


                # ======================================
                # CLAN LOGIN SUCCESS
                # ======================================

                request.session["user_type"] = "clan"
                request.session["clan_id"] = clan.id

                return redirect("clan_dashboard")


            except ClanRegistration.DoesNotExist:

                messages.error(
                    request,
                    "Invalid clan name or password."
                )

    return render(request, "Guest/login.html")

# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            auth_login(request, user)

            # Admin session
            request.session["is_admin_logged_in"] = True
            request.session["admin_username"] = user.username
            request.session["role"] = "admin"

            # 30 minutes
            request.session.set_expiry(1800)

            return redirect("admin_dashboard")

        messages.error(
            request,
            "Invalid admin username or password."
        )

    return render(
        request,
        "Guest/admin_login.html"
    )


# =========================================================
# ADMIN LOGIN CHECK
# =========================================================

def admin_logged_in(request):

    return request.session.get("is_admin_logged_in", False)


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard(request):

    if not admin_logged_in(request):
        return redirect("admin_login")

    total_players = PlayerRegistration.objects.count()

    clans = ClanRegistration.objects.all().order_by("-id")

    total_clans = clans.count()

    verified_clans = clans.filter(
        is_verified=True
    ).count()

    pending_clans = clans.filter(
        is_verified=False
    ).count()

    context = {
        "total_players": total_players,
        "total_clans": total_clans,
        "verified_clans": verified_clans,
        "pending_clans": pending_clans,
        "clans": clans,
    }

    return render(
        request,
        "Guest/admin_dashboard.html",
        context
    )


# =========================================================
# PLAYER DETAILS
# =========================================================

def player_details(request):

    if not admin_logged_in(request):
        return redirect("admin_login")

    players = PlayerRegistration.objects.all().order_by("-id")

    return render(
        request,
        "Guest/player_details.html",
        {
            "players": players
        }
    )


# =========================================================
# ALL CLANS
# =========================================================

def clan_list(request):

    if not admin_logged_in(request):
        return redirect("admin_login")

    clans = ClanRegistration.objects.all().order_by("-id")

    return render(
        request,
        "Guest/clan_list.html",
        {
            "clans": clans
        }
    )


# =========================================================
# CLAN DETAILS
# =========================================================

def clan_details(request, clan_id):

    if not admin_logged_in(request):
        return redirect("admin_login")

    clan = get_object_or_404(
        ClanRegistration,
        id=clan_id
    )

    return render(
        request,
        "Guest/clan_details.html",
        {
            "clan": clan
        }
    )


# =========================================================
# PENDING CLAN VERIFICATION
# =========================================================

def clan_verification(request):

    if not admin_logged_in(request):
        return redirect("admin_login")

    clans = ClanRegistration.objects.filter(
        is_verified=False
    ).order_by("-id")

    return render(
        request,
        "Guest/clan_verification.html",
        {
            "clans": clans
        }
    )


# =========================================================
# VERIFIED CLANS
# =========================================================

def verified_clans(request):

    if not admin_logged_in(request):
        return redirect("admin_login")

    clans = ClanRegistration.objects.filter(
        is_verified=True
    ).order_by("-id")

    return render(
        request,
        "Guest/verified_clans.html",
        {"clans": clans}
    )

# =========================================================
# VERIFY CLAN
# =========================================================

def verify_clan(request, clan_id):

    if not request.session.get("is_admin_logged_in"):
        return redirect("admin_login")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)

        clan.is_verified = True
        clan.save()

        messages.success(
            request,
            f"{clan.clan_name} has been verified successfully."
        )

    except ClanRegistration.DoesNotExist:

        messages.error(
            request,
            "Clan not found."
        )

    return redirect("clan_verification")


# =========================================================
# REJECT CLAN
# =========================================================

def reject_clan(request, clan_id):

    if not admin_logged_in(request):
        return redirect("admin_login")

    clan = get_object_or_404(
        ClanRegistration,
        id=clan_id
    )

    clan.is_verified = False
    clan.save()

    messages.warning(
        request,
        f"{clan.clan_name} verification has been rejected."
    )

    return redirect("clan_verification")


def unverify_clan(request, clan_id):

    if not request.session.get("is_admin_logged_in"):
        return redirect("admin_login")

    try:
        clan = ClanRegistration.objects.get(id=clan_id)

        clan.is_verified = False
        clan.save()

        messages.success(
            request,
            f"{clan.clan_name} verification has been removed."
        )

    except ClanRegistration.DoesNotExist:

        messages.error(
            request,
            "Clan not found."
        )

    return redirect("clan_verification")


# =========================================================
# ADMIN LOGOUT
# =========================================================

def admin_logout(request):

    request.session.flush()

    return redirect("admin_login")
# =========================================================
# LOGOUT
# =========================================================

def logout(request):

    request.session.flush()

    return redirect("login")
