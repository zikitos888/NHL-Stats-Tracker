from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Player, Team, PlayerSeasonStat
from .forms import PlayerFilterForm


class PlayerListView(ListView):
    model = Player
    template_name = 'nhlapp/player_list.html'
    context_object_name = 'players'
    paginate_by = 50

    def get_queryset(self):
        qs = Player.objects.prefetch_related(
            Prefetch('teams'),
            Prefetch('playerseasonstat_set',
                     queryset=PlayerSeasonStat.objects.order_by('-season_id'),
                     to_attr='latest_stats')
        ).distinct()

        form = PlayerFilterForm(self.request.GET)
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
                qs = qs.filter(playerseasonstat__points__gte=min_points).distinct()

        return qs.order_by('full_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PlayerFilterForm(self.request.GET)
        return context


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'nhlapp/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self.object.playerseasonstat_set.order_by('-season_id')
        context['current_teams'] = self.object.teams.all()
        return context
