from django.contrib import admin
from .models import Team, Player, PlayerSeasonStat, PlayerSeasonTeam
from django.core.management import call_command
from django.contrib import messages


class PlayerSeasonTeamInline(admin.TabularInline):
    model = PlayerSeasonTeam
    extra = 1
    autocomplete_fields = ['team']


@admin.register(PlayerSeasonStat)
class PlayerSeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season_id', 'points', 'goals', 'assists', 'games_played')
    list_filter = ('season_id',)
    search_fields = ('player__full_name',)
    inlines = [PlayerSeasonTeamInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'last_name', 'position', 'shoots_catches')
    search_fields = ('full_name', 'last_name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbrev', 'conference', 'division')
    search_fields = ('name', 'abbrev')

    actions = ['update_nhl_stats']

    def update_nhl_stats(self, request, queryset):
        try:
            call_command('load_nhl_stats', '20252026')
            self.message_user(request, 'Статистика NHL обновлена (сезон 20252026)',
                              level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f'Ошибка обновления: {str(e)}',
                              level=messages.ERROR)
        return None

    update_nhl_stats.short_description = 'Обновить статистику NHL (сезон 20252026)'
