from cricket.api.views.cricket_info import *

version = 1

views = [
    TeamListCreateView,
    PlayerListCreateView,
    MatchListCreateView,
    ScoreListCreateView,
    PlayerUpdateDetailView,
    PlayerDeleteView,
    TournamentListCreateView,
    TeamDetailView,
    TeamDeleteView,
    PlayersTeamView,
    TournamentTeamView,
    MatchWinnerView
]

urlpatterns = []
[urlpatterns.extend(view.urlpatterns(version)) for view in views]