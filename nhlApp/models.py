from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=10)
    conference = models.CharField(max_length=20)
    division = models.CharField(max_length=20)
    external_id = models.IntegerField()

    FULL_NAMES = {
        'ARI': 'Аризона Койотиз',
        'EDM': 'Эдмонтон Ойлерз',
        'COL': 'Колорадо Эвеланш',
        'SEA': 'Сиэтл Кракен',
        'MTL': 'Монреаль Канадиенс',
        'PIT': 'Питтсбург Пингвинз',
        'BUF': 'Баффало Сэйбрз',
        'MIN': 'Миннесота Уайлд',
        'NYR': 'Нью-Йорк Рейнджерс',
        'BOS': 'Бостон Брюинз',
        'DAL': 'Даллас Старз',
        'OTT': 'Оттава Сенаторз',
        'CHI': 'Чикаго Блэкхокс',
        'CGY': 'Калгари Флэймз',
        'VAN': 'Ванкувер Кэнакс',
        'ANA': 'Анахайм Дакс',
        'STL': 'Сент-Луис Блюз',
        'TOR': 'Торонто Мэйпл Лифс',
        'NJD': 'Нью-Джерси Дэвилз',
        'DET': 'Детройт Ред Уингз',
        'SJS': 'Сан-Хосе Шаркс',
        'PHI': 'Филадельфия Флайерз',
        'WPG': 'Виннипег Джетс',
        'LAK': 'Лос-Анджелес Кингз',
        'TBL': 'Тампа-Бэй Лайтнинг',
        'VGK': 'Вегас Голден Найтс',
        'NSH': 'Нэшвилл Предаторз',
        'CAR': 'Каролина Харрикейнз',
        'CBJ': 'Коламбус Блю Джекетс',
        'NYI': 'Нью-Йорк Айлендерс',
        'FLA': 'Флорида Пантерз',
        'UTA': 'Юта Хоккей Клаб',
        'WSH': 'Вашингтон Кэпиталз',
    }

    def full_name(self):
        return self.FULL_NAMES.get(self.abbrev, self.name)

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
        return self.teams.all().select_related('team')  # Оптимизация

    def clear_teams(self):
        PlayerSeasonTeam.objects.filter(player_season_stat=self).delete()


class PlayerSeasonTeam(models.Model):
    player_season_stat = models.ForeignKey(PlayerSeasonStat, on_delete=models.CASCADE, related_name='teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('player_season_stat', 'team')

    def __str__(self):
        return f"{self.player_season_stat} - {self.team.name}"
