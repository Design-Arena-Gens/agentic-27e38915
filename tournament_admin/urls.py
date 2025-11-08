from django.contrib.auth.views import LogoutView
from django.urls import path

from tournament_admin import views

app_name = 'tournament_admin'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='tournament_admin:login'), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('tournaments/new/', views.create_tournament, name='create_tournament'),
    path('teams/new/', views.create_team, name='create_team'),
    path('teams/assign/', views.assign_players, name='assign_players'),
]
