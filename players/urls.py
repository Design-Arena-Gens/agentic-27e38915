from django.urls import path

from players import views

app_name = 'players'

urlpatterns = [
    path('', views.register_player, name='register'),
    path('success/<str:registration_number>/', views.registration_success, name='registration_success'),
    path('lookup/', views.search_player, name='search'),
]
