from django.db import models

# Create your models here.

class PlayerRegistration(models.Model):

    GAME_MODE_CHOICES = [('solo', 'Solo'),('duo', 'Duo'),('squad', 'Squad'),]

    PLAYER_ROLE_CHOICES = [('assault', 'Assault'),('sniper', 'Sniper'),('support', 'Support'),('igl', 'IGL'),]

    # Player Information
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)

    # BGMI Information
    bgmi_id = models.CharField(max_length=50, unique=True)
    in_game_name = models.CharField(max_length=100)

    game_mode = models.CharField(max_length=10,choices=GAME_MODE_CHOICES)

    player_role = models.CharField(max_length=20,choices=PLAYER_ROLE_CHOICES,blank=True,null=True)

    # Profile
    profile_image = models.ImageField(upload_to='player_profiles/',blank=True,null=True)

    # Account Security
    password = models.CharField(max_length=128)

    # Date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class ClanRegistration(models.Model):

    CLAN_TYPE_CHOICES = [
        ('competitive', 'Competitive'),
        ('casual', 'Casual'),
        ('esports', 'Esports'),
    ]

    GAME_MODE_CHOICES = [
        ('duo', 'Duo'),
        ('squad', 'Squad'),
    ]

    MEMBER_COUNT_CHOICES = [
        (2, '2 Members'),
        (3, '3 Members'),
        (4, '4 Members'),
    ]

    # Clan Information
    clan_name = models.CharField(max_length=100)
    clan_tag = models.CharField(max_length=6, unique=True)

    captain_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=10)

    clan_type = models.CharField(
        max_length=20,
        choices=CLAN_TYPE_CHOICES
    )

    # BGMI Details
    captain_bgmi_id = models.CharField(
        max_length=50,
        unique=True
    )

    game_mode = models.CharField(
        max_length=10,
        choices=GAME_MODE_CHOICES
    )

    member_count = models.PositiveIntegerField(
        choices=MEMBER_COUNT_CHOICES
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # Clan Description
    description = models.TextField(
        blank=True,
        null=True
    )

    # Clan Logo
    clan_logo = models.ImageField(
        upload_to='clan_logos/',
        blank=True,
        null=True
    )

    # Account Security
    password = models.CharField(max_length=128)

    # Verification
    is_verified = models.BooleanField(default=False)

    # Date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.clan_name



    