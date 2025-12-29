from django import forms
from .models import Player, Team

POSITION_CHOICES = (
    ('', 'Все'), ('C', 'C'), ('L', 'L'), ('R', 'R'), ('D', 'D'), ('G', 'G'),
)

SEASON_CHOICES = [
    ('20252026', '2025/26'),
    ('20242025', '2024/25'),
    ('20232024', '2023/24'),
    ('20222023', '2022/23'),
    ('20212022', '2021/22'),
    ('20202021', '2020/21'),
]


class PlayerFilterForm(forms.Form):
    name = forms.CharField(label='Имя', required=False, max_length=100)
    position = forms.ChoiceField(label='Позиция', choices=POSITION_CHOICES, required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label='Команда', required=False, empty_label='Все')

    season_id = forms.ChoiceField(
        label='Сезон',
        choices=SEASON_CHOICES,
        initial='20252026',
        required=False
    )
    min_points = forms.IntegerField(label='Мин. очков', required=False)
