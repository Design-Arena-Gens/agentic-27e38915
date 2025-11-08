from django.contrib import admin

from tournament_admin.models import Team, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'location')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'mentor')
    list_filter = ('tournament',)
    search_fields = ('name', 'mentor')
