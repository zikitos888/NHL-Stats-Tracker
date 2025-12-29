from django.views.generic import ListView, DetailView
from django.db.models import Prefetch, Subquery, OuterRef, Exists
from .models import Player, Team, PlayerSeasonStat
from .forms import PlayerFilterForm
from django.db.models import Q, Max


class PlayerListView(ListView):
    model = Player
    template_name = 'nhlapp/player_list.html'
    context_object_name = 'players'
    paginate_by = 50

    def get_queryset(self):
        form = PlayerFilterForm(self.request.GET)
        season_filter = form.data.get('season_id', '20252026')

        has_stats_in_season = Exists(PlayerSeasonStat.objects.filter(
            player=OuterRef('pk'),
            season_id=season_filter,
            games_played__gt=0
        ))

        stat_prefetch = Prefetch(
            'playerseasonstat_set',
            queryset=PlayerSeasonStat.objects.filter(season_id=season_filter),
            to_attr='season_stats'
        )

        qs = Player.objects.prefetch_related(
            Prefetch('teams'),
            stat_prefetch
        ).filter(has_stats_in_season).distinct()

        if form.is_valid():
            name = form.cleaned_data.get('name')
            position = form.cleaned_data.get('position')
            team = form.cleaned_data.get('team')
            min_points = form.cleaned_data.get('min_points')

            if name:
                qs = qs.filter(full_name__icontains=name)
            if position:
                qs = qs.filter(position=position)
            if team:
                qs = qs.filter(teams=team)

            if min_points:
                qs = qs.annotate(
                    season_points=Max('playerseasonstat__points',
                                      filter = Q(playerseasonstat__season_id=season_filter))
                ).filter(season_points__gte=min_points)

        sort_by = self.request.GET.get('sort', 'name')
        if sort_by == 'points':
            qs = qs.annotate(
                season_points=Max('playerseasonstat__points',
                                  filter = Q(playerseasonstat__season_id=season_filter))
            ).order_by('-season_points', 'full_name')
        else:
            qs = qs.order_by('full_name')

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PlayerFilterForm(self.request.GET or {'season_id': '20252026'})
        context['selected_season'] = self.request.GET.get('season_id', '20252026')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page', None)
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
