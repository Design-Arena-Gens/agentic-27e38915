from django import forms

from players.models import Player
from tournament_admin.models import Team, Tournament


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'location', 'description', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['name', 'location']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['tournament', 'name', 'mentor', 'logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).order_by('start_date')
        self.fields['tournament'].widget.attrs.update({'class': 'form-select'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['mentor'].widget.attrs.update({'class': 'form-control'})
        self.fields['logo'].widget.attrs.update({'class': 'form-control'})


class TeamAssignmentForm(forms.Form):
    tournament = forms.ModelChoiceField(
        queryset=Tournament.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 10}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tournament'].queryset = Tournament.objects.filter(is_active=True).order_by('start_date')
        tournament = None
        tournament_id = self.data.get('tournament')
        if tournament_id:
            try:
                tournament = Tournament.objects.get(pk=tournament_id)
            except Tournament.DoesNotExist:
                tournament = None
        elif self.initial.get('tournament'):
            initial_value = self.initial.get('tournament')
            if isinstance(initial_value, Tournament):
                tournament = initial_value
            else:
                try:
                    tournament = Tournament.objects.get(pk=initial_value)
                except Tournament.DoesNotExist:
                    tournament = None

        if tournament:
            self.fields['team'].queryset = tournament.teams.all()
            eligible_players = Player.objects.filter(tournament=tournament, consent_to_play=True).order_by('full_name')
            self.fields['players'].queryset = eligible_players
        else:
            self.fields['team'].queryset = Team.objects.none()
            self.fields['players'].queryset = Player.objects.none()
