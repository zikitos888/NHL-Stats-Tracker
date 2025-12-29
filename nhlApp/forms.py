from django import forms
from .models import Player, Team

POSITION_CHOICES = (
    ('', 'Все'), ('C', 'C'), ('L', 'L'), ('R', 'R'), ('D', 'D'), ('G', 'G'),
)

class PlayerFilterForm(forms.Form):
    name = forms.CharField(label='Имя', required=False, max_length=100)
    position = forms.ChoiceField(label='Позиция', choices=POSITION_CHOICES, required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label='Команда', required=False, empty_label='Все')
    min_points = forms.IntegerField(label='Мин. очков', required=False)
