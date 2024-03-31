from django.urls import path
from . import views


urlpatterns = [
    path('filter/<str:salary_amount>/', views.filter_vacancies_by_salary, name='filter_vacancies_by_salary'),
    path('leagues/', views.LeagueListView.as_view(), name='league-list'),
    path('leagues/<int:pk>/', views.LeagueDetailView.as_view(), name='league-detail'),
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('players/', views.PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', views.PlayerDetailView.as_view(), name='player-detail'),
    path('matches/', views.MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', views.MatchDetailView.as_view(), name='match-detail'),
    path('standings/', views.StandingListView.as_view(), name='standing-list'),
    path('standings/<int:pk>/', views.StandingDetailView.as_view(), name='standing-detail'),
]
