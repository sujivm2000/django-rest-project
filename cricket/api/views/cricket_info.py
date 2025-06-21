from django.views.generic.edit import BaseDeleteView
from rest_framework.response import Response
from rest_framework import status
from base.api.views import (
    BaseListCreateView, BaseUpdateDetailView, BaseDestroyView, BaseListView, BaseDetailView
)
from cricket.api.serializers.cricket_info import *
from cricket.models.cricket_info import *
from django.db.models import Q


class TeamListCreateView(BaseListCreateView):
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if Team.objects.filter(name__iexact=data['name']).exists():
            return Response({'error': f'Team already exist'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class PlayerListCreateView(BaseListCreateView):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        team = data.get('team')
        if not team:
            return Response({'error': 'Team is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not Team.objects.filter(id=team).exists():
            return Response({'error': 'Team does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        team_instance = Team.objects.get(id=team)
        request.data['team'] = str(team_instance.id)
        return super().create(request, *args, **kwargs)


class MatchListCreateView(BaseListCreateView):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        team1 = data.get('team1')
        team2 = data.get('team2')

        if team1 == team2:
            return Response({'error': 'Both teams cannot be same'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class ScoreListCreateView(BaseListCreateView):
    serializer_class = ScoreSerialixzer
    queryset = ScoreCard.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        player_id = data['player']
        match_id=data['match']
        match_instance=Match.objects.get(id=match_id)
        scorecard_instance=ScoreCard.objects.select_related('player','match').get(match=match_id,player=player_id)
        if scorecard_instance:
            return Response({'info': f'score associated with this match of {scorecard_instance.player.name} has already updated'}, status=status.HTTP_400_BAD_REQUEST)
        if not Player.objects.select_related('team').filter(Q(id=player_id) & Q(team__id__in=[match_instance.team1.id,match_instance.team2.id])).exists():
            return Response({'error': 'player does not belong to either of the team'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request,*args,**kwargs)


class PlayerUpdateDetailView(BaseUpdateDetailView):
    serializer_class = PlayerUpdateDetaiSerializer
    queryset = Player.objects.all()

    def update(self, request, *args, **kwargs):
        super().update(request,*args,**kwargs)
        return Response(
            {"message": "Player updated successfully"},
            status=status.HTTP_200_OK
        )

class PlayerDeleteView(BaseDestroyView):
    serializer_class=PlayerDeleteSerializer

    def delete(self, request, *args, **kwargs):
        super().delete(request,*args,**kwargs)
        return Response({"message: item deleted successfullt"},status=status.HTTP_204_NO_CONTENT)


class TournamentListCreateView(BaseListCreateView):
    serializer_class=TournamentListCreateSerializer
    queryset=Tournament.objects.all()

    def create(self, request, *args, **kwargs):
        data=request.data
        tournament_name=data.get('name')
        tournament_year=data.get('year')
        if Tournament.objects.filter(name__iexact=tournament_name,year=tournament_year).exists():
            return Response({'error':'Tournment already exists'},startus=status.HTTP_400_BAD_REQUEST)
        return super().create(request,*args,**kwargs)

class TeamDetailView(BaseUpdateDetailView):
    serializer_class=TeamSerializer
    queryset=Team.objects.all()

    def update(self, request, *args, **kwargs):
        super().update(request,*args,**kwargs)
        return Response(
            {"message": "Team updated successfully"
             },
            status=status.HTTP_200_OK
        )

class TeamDeleteView(BaseDestroyView):
    serializer_class = TeamDeleteSerializer

    def delete(self, request, *args, **kwargs):
        super().delete(request,*args,**kwargs)
        return Response({"message: item deleted successfullt"},status=status.HTTP_204_NO_CONTENT)

class PlayerListByTeamView(BaseListView):
    serializer_class = AssociateTeamPlayerSerializer
    url_path = '/<int:id>/players'
    def get_queryset(self):
        team_id=self.kwargs.get('team_id')
        return Player.object.filter(team__id=team_id)

class PlayersTeamView(BaseListView):
    url_path = '/team/<int:id>/'
    serializer_class = PlayersTeamSerializer

    def get_queryset(self):
        team_id=self.kwargs.get('id')
        return Player.objects.filter(team_id=team_id)

    def list(self,request,*args,**kwargs):
        team_id=self.kwargs.get('id','')
        if not Team.objects.filter(id=team_id).exists():
            return Response({"message":f"team with id:{team_id} doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        return super().list(request,*args,**kwargs)


class TournamentTeamView(BaseListView):
    url_path = '/tournaments/<int:id>/'
    serializer_class = TournamentTeamsSerializer

    def get_queryset(self):
        tournament_id=self.kwargs.get('id')
        return Match.objects.filter(tournament_id=tournament_id)

    def list(self, request, *args, **kwargs):
        tournament_id = self.kwargs.get('id')
        if not Tournament.objects.filter(id=tournament_id).exists():
            return Response({"message": f"Tournament with id:{tournament_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        return super().list(self,request,*args,**kwargs)

class MatchWinnerView(BaseListView):
    url_path = '/winners/'
    view_name = 'matchwinners'
    serializer_class = MatchWinnerSerializer

    def get_queryset(self):
        return Match.objects.select_related('winner').filter(winner__isnull=False)

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if not queryset:
            return Response({"message":"No winner found"},status=status.HTTP_400_BAD_REQUEST)
        return super().list(request,*args,**kwargs)

class ReadPdfAttached(BaseListView):
    pass
