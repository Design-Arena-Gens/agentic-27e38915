from django import forms

from players.models import Player
from tournament_admin.models import Tournament


class PlayerRegistrationForm(forms.ModelForm):
    """Form for capturing player registration details."""

    consent_to_play = forms.BooleanField(
        label='I agree to participate in the selected tournament.',
        required=True,
    )

    class Meta:
        model = Player
        fields = [
            'full_name',
            'date_of_birth',
            'gender',
            'playing_position',
            'photo',
            'institution_name',
            'tournament',
            'consent_to_play',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'playing_position': forms.Select(attrs={'class': 'form-select'}),
            'tournament': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_tournaments = Tournament.objects.filter(is_active=True).order_by('start_date')
        self.fields['tournament'].queryset = active_tournaments
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['institution_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['consent_to_play'].widget.attrs.update({'class': 'form-check-input'})
