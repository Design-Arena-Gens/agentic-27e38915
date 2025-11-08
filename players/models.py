import random
from datetime import date

from django.db import models


class Player(models.Model):
    """Represents a registered netball player."""

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-binary'),
    ]

    POSITION_CHOICES = [
        ('GS', 'Goal Shooter'),
        ('GA', 'Goal Attack'),
        ('WA', 'Wing Attack'),
        ('C', 'Centre'),
        ('WD', 'Wing Defence'),
        ('GD', 'Goal Defence'),
        ('GK', 'Goal Keeper'),
    ]

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    playing_position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    photo = models.ImageField(
        upload_to='player_photos/',
        blank=True,
        default='defaults/player-placeholder.png',
    )
    institution_name = models.CharField(max_length=255)
    tournament = models.ForeignKey(
        'tournament_admin.Tournament',
        on_delete=models.CASCADE,
        related_name='registered_players',
    )
    consent_to_play = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self) -> str:
        return f'{self.full_name} ({self.registration_number})'

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = self._generate_registration_number()
        super().save(*args, **kwargs)

    def _generate_registration_number(self) -> str:
        """Generate a unique four-digit identifier."""
        model = self.__class__
        while True:
            number = f'{random.randint(0, 9999):04d}'
            if not model.objects.filter(registration_number=number).exists():
                return number

    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )
