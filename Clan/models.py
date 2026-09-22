from decimal import Decimal
from django.db import models
from Guest.models import ClanRegistration, PlayerRegistration


from decimal import Decimal
from django.db import models
from Guest.models import ClanRegistration, PlayerRegistration


class Tournament(models.Model):

    MAP_CHOICES = [
        ("Erangel", "Erangel"),
        ("Miramar", "Miramar"),
        ("Sanhok", "Sanhok"),
        ("Livik", "Livik"),
        ("Rondo", "Rondo"),
        ("Vikendi", "Vikendi"),
    ]

    GAME_MODE_CHOICES = [
        ("Solo", "Solo"),
        ("Duo", "Duo"),
        ("Squad", "Squad"),
    ]

    clan = models.ForeignKey(
        ClanRegistration,
        on_delete=models.CASCADE,
        related_name="tournaments"
    )

    tournament_name = models.CharField(max_length=200)

    map = models.CharField(
        max_length=50,
        choices=MAP_CHOICES
    )

    game_mode = models.CharField(
        max_length=20,
        choices=GAME_MODE_CHOICES
    )

    tournament_date = models.DateField()

    tournament_time = models.TimeField()

    entry_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    prize_pool = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    # NEW PRIZE FIELDS
    first_prize = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    second_prize = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    third_prize = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    matches = models.PositiveIntegerField(default=1)

    total_slot = models.PositiveIntegerField(default=1)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tournament_name


class Booking(models.Model):

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    player = models.ForeignKey(
        PlayerRegistration,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    player_name = models.CharField(max_length=200)

    bgmi_id = models.CharField(max_length=100)

    in_game_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    game_mode = models.CharField(max_length=50)

    slot_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        default="Booked"
    )

    room_token = models.UUIDField(
        null=True,
        blank=True,
        editable=False
    )

    tournament_link = models.URLField(max_length=500, null=True, blank=True)

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.player_name} - {self.tournament.tournament_name}"