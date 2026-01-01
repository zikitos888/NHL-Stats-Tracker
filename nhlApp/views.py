from django.views.generic import ListView, DetailView
from django.db.models import Prefetch, OuterRef, Exists, Max, Q
from .models import Player, PlayerSeasonStat
from .forms import PlayerFilterForm


class PlayerListView(ListView):
    model = Player
    template_name = 'nhlapp/player_list.html'
    context_object_name = 'players'
    paginate_by = 50

    def get_queryset(self):
        form = PlayerFilterForm(self.request.GET)
        season_filter = form.data.get('season_id', '20252026')

        has_stats_in_season = Exists(
            PlayerSeasonStat.objects.filter(
                player=OuterRef('pk'),
                season_id=season_filter,
                games_played__gt=0
            )
        )

        stat_prefetch = Prefetch(
            'playerseasonstat_set',
            queryset=PlayerSeasonStat.objects.filter(season_id=season_filter),
            to_attr='season_stats'
        )

        qs = (
            Player.objects
            .filter(has_stats_in_season)
            .prefetch_related('teams', stat_prefetch)
            .annotate(
                season_games=Max(
                    'playerseasonstat__games_played',
                    filter=Q(playerseasonstat__season_id=season_filter)
                ),
                season_goals=Max(
                    'playerseasonstat__goals',
                    filter=Q(playerseasonstat__season_id=season_filter)
                ),
                season_assists=Max(
                    'playerseasonstat__assists',
                    filter=Q(playerseasonstat__season_id=season_filter)
                ),
                season_points=Max(
                    'playerseasonstat__points',
                    filter=Q(playerseasonstat__season_id=season_filter)
                ),
            )
            .distinct()
        )

        if form.is_valid():
            if form.cleaned_data.get('name'):
                qs = qs.filter(full_name__icontains=form.cleaned_data['name'])
            if form.cleaned_data.get('position'):
                qs = qs.filter(position=form.cleaned_data['position'])
            if form.cleaned_data.get('team'):
                qs = qs.filter(teams=form.cleaned_data['team'])
            if form.cleaned_data.get('min_points'):
                qs = qs.filter(season_points__gte=form.cleaned_data['min_points'])

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        sort_map = {
            'name': 'full_name',
            'position': 'position',
            'team': 'teams__abbrev',
            'games': 'season_games',
            'goals': 'season_goals',
            'assists': 'season_assists',
            'points': 'season_points',
        }

        sort_field = sort_map.get(sort, 'full_name')
        if order == 'desc':
            sort_field = f'-{sort_field}'

        qs = qs.order_by(sort_field, 'full_name')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = PlayerFilterForm(
            self.request.GET or {'season_id': '20252026'}
        )

        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['current_order'] = self.request.GET.get('order', 'asc')

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        query_params.pop('sort', None)
        query_params.pop('order', None)

        context['query_params'] = query_params.urlencode()

        return context


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'nhlapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self.object.playerseasonstat_set.order_by('-season_id')
        context['current_teams'] = self.object.teams.all()
        return context
