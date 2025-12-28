from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=10)
    conference = models.CharField(max_length=20)
    division = models.CharField(max_length=20)
    external_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    full_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=1)
    shoots_catches = models.CharField(max_length=1)
    external_id = models.IntegerField(unique=True)
    teams = models.ManyToManyField(Team, related_name='players')

    def __str__(self):
        return self.full_name

class PlayerSeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season_id = models.CharField(max_length=10)
    games_played = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    points = models.IntegerField()
    plus_minus = models.IntegerField()
    shots = models.IntegerField()
    shooting_pct = models.FloatField()
    pp_goals = models.IntegerField()
    pp_points = models.IntegerField()
    sh_goals = models.IntegerField()
    sh_points = models.IntegerField()
    ev_goals = models.IntegerField()
    ev_points = models.IntegerField()
    time_on_ice_per_game = models.FloatField()
    faceoff_win_pct = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('player', 'season_id')