from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=10)
    conference = models.CharField(max_length=20)
    division = models.CharField(max_length=20)
    external_id = models.IntegerField()

    def __str__(self):
        return self.name

class Player(models.Model):
    full_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=1)
    shoots_catches = models.CharField(max_length=1)
    external_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.full_name

class PlayerSeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season_id = models.CharField(max_length=10)
    games_played = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()
    plus_minus = models.IntegerField(null=True, blank=True)
    shots = models.IntegerField(null=True, blank=True)
    shooting_pct = models.FloatField(null=True, blank=True)
    pp_goals = models.IntegerField(null=True, blank=True)
    pp_points = models.IntegerField(null=True, blank=True)
    sh_goals = models.IntegerField(null=True, blank=True)
    sh_points = models.IntegerField(null=True, blank=True)
    ev_goals = models.IntegerField(null=True, blank=True)
    ev_points = models.IntegerField(null=True, blank=True)
    time_on_ice_per_game = models.FloatField(null=True, blank=True)
    faceoff_win_pct = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('player', 'season_id')

    def __str__(self):
        return f'{self.player.full_name} - {self.season_id}'

    @property
    def teams(self):
        """Возвращает команды, в которых игрок играл в этом сезоне"""
        return self.teams.all().select_related('team')  # Оптимизация

    def clear_teams(self):
        """Очищает все связи с командами для этого сезона"""
        PlayerSeasonTeam.objects.filter(player_season_stat=self).delete()


class PlayerSeasonTeam(models.Model):
    player_season_stat = models.ForeignKey(PlayerSeasonStat, on_delete=models.CASCADE, related_name='teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('player_season_stat', 'team')

    def __str__(self):
        return f"{self.player_season_stat} - {self.team.name}"
