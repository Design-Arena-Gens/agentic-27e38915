from django.db import models


class Tournament(models.Model):
    """Competitive event that players can opt into."""

    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date', 'name']

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    """Represents a tournament team with assigned players."""

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='teams',
    )
    name = models.CharField(max_length=255)
    mentor = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(
        upload_to='team_logos/',
        blank=True,
        default='defaults/team-placeholder.png',
    )
    players = models.ManyToManyField(
        'players.Player',
        related_name='teams',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tournament', 'name')
        ordering = ['tournament__name', 'name']

    def __str__(self) -> str:
        return f'{self.name} ({self.tournament.name})'

# Create your models here.
