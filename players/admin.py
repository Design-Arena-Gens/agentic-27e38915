from django.contrib import admin

from players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'registration_number', 'tournament', 'playing_position', 'gender', 'created_at')
    search_fields = ('full_name', 'registration_number', 'institution_name')
    list_filter = ('tournament', 'gender', 'playing_position')
