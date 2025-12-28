import math
import requests

from django.core.management.base import BaseCommand
from nhlApp.models import Team, Player, PlayerSeasonStat


BASE_URL = "https://api.nhle.com/stats/rest/en/skater/summary"
SEASON_ID = "20252026"


class Command(BaseCommand):
    help = "Load NHL skater nhlApp for a season from NHL API"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(f"Loading nhlApp for season {SEASON_ID}"))

        params = {
            "cayenneExp": f"seasonId={SEASON_ID} and gameTypeId=2",
            "start": 0,
            "limit": 50,
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        total = data.get("total", 0)
        self.stdout.write(f"Total players reported by API: {total}")

        if total == 0:
            self.stdout.write(self.style.WARNING("No data returned from API"))
            return

        pages = math.ceil(total / params["limit"])

        for page in range(pages):
            start = page * params["limit"]
            self.stdout.write(f"Fetching page {page + 1}/{pages} (start={start})")

            page_params = params | {"start": start}
            resp = requests.get(BASE_URL, params=page_params, timeout=10)
            resp.raise_for_status()
            page_data = resp.json()
            for item in page_data.get("data", []):
                self._save_player_and_stats(item)

        self.stdout.write(self.style.SUCCESS("NHL nhlApp loaded successfully"))

    def _save_player_and_stats(self, item: dict):
        team_abbrevs = item.get("teamAbbrevs") or ""
        main_team_abbrev = team_abbrevs.split(",")[0] if team_abbrevs else None

        team = None
        if main_team_abbrev:
            team, _ = Team.objects.get_or_create(
                abbrev=main_team_abbrev,
                defaults={
                    "name": main_team_abbrev,
                    "conference": "",
                    "division": "",
                    "external_id": 0,
                },
            )

        player_id = item["playerId"]
        full_name = item["skaterFullName"]
        last_name = item["lastName"]
        position = item["positionCode"]
        shoots_catches = item.get("shootsCatches") or ""

        player, _ = Player.objects.get_or_create(
            external_id=player_id,
            defaults={
                "full_name": full_name,
                "last_name": last_name,
                "position": position,
                "shoots_catches": shoots_catches,
            },
        )
        if team:
            player.teams.add(team)

        stats, _ = PlayerSeasonStat.objects.update_or_create(
            player=player,
            season_id=str(item["seasonId"]),
            defaults={
                "games_played": item["gamesPlayed"],
                "goals": item["goals"],
                "assists": item["assists"],
                "points": item["points"],
                "plus_minus": item["plusMinus"],
                "shots": item["shots"],
                "shooting_pct": item.get("shootingPct"),
                "pp_goals": item["ppGoals"],
                "pp_points": item["ppPoints"],
                "sh_goals": item["shGoals"],
                "sh_points": item["shPoints"],
                "ev_goals": item["evGoals"],
                "ev_points": item["evPoints"],
                "time_on_ice_per_game": item["timeOnIcePerGame"],
                "faceoff_win_pct": item.get("faceoffWinPct"),
            },
        )