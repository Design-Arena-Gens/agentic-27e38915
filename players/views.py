from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from players.forms import PlayerRegistrationForm
from players.models import Player


@require_http_methods(['GET', 'POST', 'HEAD'])
def register_player(request):
    """Handle player registration."""
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save()
            return redirect('players:registration_success', registration_number=player.registration_number)
    else:
        form = PlayerRegistrationForm()

    return render(request, 'players/register.html', {'form': form})


def registration_success(request, registration_number: str):
    """Show the registration number confirmation screen."""
    player = get_object_or_404(Player, registration_number=registration_number)
    return render(
        request,
        'players/registration_success.html',
        {'player': player},
    )


def search_player(request):
    """Lookup a player by registration number via HTMX or a full page."""
    registration_number = request.GET.get('registration_number', '').strip()
    player = None
    if registration_number and registration_number.isdigit():
        registration_number = registration_number.zfill(4)
        player = Player.objects.filter(registration_number=registration_number).select_related('tournament').first()

    template_name = (
        'players/partials/search_result.html'
        if getattr(request, 'htmx', False)
        else 'players/search.html'
    )

    return render(
        request,
        template_name,
        {
            'player': player,
            'registration_number': registration_number,
        },
    )
