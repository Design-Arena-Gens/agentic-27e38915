from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from players.models import Player
from tournament_admin.forms import TeamAssignmentForm, TeamForm, TournamentForm
from tournament_admin.models import Team, Tournament


class AdminLoginView(LoginView):
    """Custom login view for tournament administrators."""

    template_name = 'tournament_admin/login.html'
    redirect_authenticated_user = True


def _filter_players(players, age_group=None, category=None):
    """Apply age group and category filters on player queryset."""
    age_limits = {
        'u14': 14,
        'u16': 16,
        'u17': 17,
        'u19': 19,
    }

    category_rules = {
        'girls': lambda player: player.gender == 'female' and player.age <= 17,
        'boys': lambda player: player.gender == 'male' and player.age <= 17,
        'women': lambda player: player.gender == 'female' and player.age > 17,
        'men': lambda player: player.gender == 'male' and player.age > 17,
    }

    filtered = []
    for player in players:
        if age_group in age_limits and player.age > age_limits[age_group]:
            continue
        if category in category_rules and not category_rules[category](player):
            continue
        filtered.append(player)
    return filtered


@login_required
def dashboard(request):
    """Show player analytics and management shortcuts."""
    age_group = request.GET.get('age_group')
    category = request.GET.get('category')

    players = list(
        Player.objects.select_related('tournament').prefetch_related('teams').order_by('full_name')
    )
    filtered_players = _filter_players(players, age_group=age_group, category=category)

    context = {
        'players': filtered_players,
        'age_group': age_group,
        'category': category,
        'tournaments': Tournament.objects.order_by('-start_date'),
        'teams': Team.objects.select_related('tournament').prefetch_related('players').order_by('tournament__name', 'name'),
        'player_count': len(filtered_players),
        'age_filters': ['u14', 'u16', 'u17', 'u19'],
        'category_filters': ['girls', 'boys', 'women', 'men'],
    }
    return render(request, 'tournament_admin/dashboard.html', context)


@login_required
def create_tournament(request):
    form = TournamentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tournament = form.save()
        messages.success(request, f'Tournament "{tournament.name}" created successfully.')
        return redirect('tournament_admin:dashboard')
    return render(request, 'tournament_admin/tournament_form.html', {'form': form})


@login_required
def create_team(request):
    form = TeamForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        team = form.save()
        messages.success(request, f'Team "{team.name}" created for {team.tournament.name}.')
        return redirect('tournament_admin:dashboard')
    return render(request, 'tournament_admin/team_form.html', {'form': form})


@login_required
def assign_players(request):
    form = TeamAssignmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        team = form.cleaned_data['team']
        players = form.cleaned_data['players']
        team.players.set(players)
        messages.success(
            request,
            f'{players.count()} player(s) assigned to {team.name}.',
        )
        return redirect('tournament_admin:dashboard')

    return render(request, 'tournament_admin/assign_players.html', {'form': form})
