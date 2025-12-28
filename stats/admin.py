from django.contrib import admin
from .models import Team, Player, PlayerSeasonStat

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbrev', 'conference', 'division')
    search_fields = ('name', 'abbrev')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'last_name', 'position', 'shoots_catches')
    search_fields = ('full_name', 'last_name')

@admin.register(PlayerSeasonStat)
class PlayerSeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season_id', 'points', 'goals', 'assists', 'games_played')
    list_filter = ('season_id',)
    search_fields = ('player__full_name',)
