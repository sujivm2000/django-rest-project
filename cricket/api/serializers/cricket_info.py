from paddle.base.libpaddle.eager.ops.legacy import instance_norm
from rest_framework import serializers

from cricket.models.cricket_info import Team, Player, Match, ScoreCard, Tournament
from rest_framework.serializers import ModelSerializer
from base.api.serializers import BaseListCreateSerializer, BaseUpdateDetailSerializer, BaseModelSerializer, \
    BaseDetailSerializer


class TeamSerializer(BaseListCreateSerializer):
    class Meta(BaseListCreateSerializer.Meta):
        model = Team
        fields = ['id', 'name', 'short_name', 'city', 'coach', 'home_ground']


class PlayerSerializer(BaseListCreateSerializer):
    class Meta(BaseListCreateSerializer.Meta):
        model = Player
        fields = ['id', 'name', 'age', 'team', 'role', 'batting_style', 'bowling_style', 'total_runs', 'total_wickets']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.team:
            representation['team'] = {
                "name": instance.team.name,
                "home-ground": instance.team.home_ground
            }
        return representation


class MatchSerializer(BaseListCreateSerializer):
    class Meta(BaseListCreateSerializer.Meta):
        model = Match
        fields = ['id', 'team1', 'team2', 'date', 'venue', 'winner', 'tournament']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.team1:
            representation['team1'] = instance.team1.name

        if instance.team2:
            representation['team2'] = instance.team2.name

        if instance.winner:
            representation['winner'] = instance.winner.name
        if instance.tournament:
            representation['tournament'] = instance.tournament.name

        return representation


class ScoreSerialixzer(BaseListCreateSerializer):
    class Meta(BaseListCreateSerializer.Meta):
        model = ScoreCard
        fields = ['match', 'player', 'runs', 'balls_faced', 'wickets', 'overs_bowled']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.match:
            representation['match'] = instance.match.team1.name + " v/s " + instance.match.team2.name
        if instance.player:
            representation['player'] = instance.player.name
        return representation


class PlayerUpdateDetaiSerializer(BaseUpdateDetailSerializer):
    class Meta(BaseUpdateDetailSerializer.Meta):
        model = Player
        fields = '__all__'


class PlayerDeleteSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Player


class TournamentListCreateSerializer(BaseListCreateSerializer):
    class Meta(BaseListCreateSerializer.Meta):
        model = Tournament
        fields = '__all__'


class TeamDeleteSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Team


class AssociateTeamPlayerSerializer(BaseListCreateSerializer):
    class Meta(BaseListCreateSerializer.Meta):
        model = Player
        fields = ['id', 'name', 'team']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.team:
            representation['team'] = instance.team.name
        return representation


class PlayersTeamSerializer(BaseListCreateSerializer):
    team_name = serializers.SerializerMethodField()

    class Meta(BaseListCreateSerializer.Meta):
        model = Player
        fields = ['id', 'name', 'age', 'team', 'role', 'batting_style', 'bowling_style', 'total_runs', 'total_wickets',
                  'team_name']

    def get_team_name(self, instance):
        return instance.team.name


class TournamentTeamsSerializer(BaseListCreateSerializer):
    tournament_name = serializers.SerializerMethodField()

    class Meta(BaseListCreateSerializer.Meta):
        model = Match
        fields = ['team1', 'team2', 'date', 'venue', 'winner', 'tournament_name']

    def get_tournament_name(self, instance):
        return instance.tournament.name


class MatchWinnerSerializer(BaseListCreateSerializer):
    winner_name = serializers.SerializerMethodField()
    tournament_name = serializers.SerializerMethodField()
    class Meta(BaseListCreateSerializer.Meta):
        model = Match
        fields = [ 'winner_name', 'tournament_name']

    def get_winner_name(self, instance):
        return instance.winner.name

    def get_tournament_name(self, instance):
        return instance.tournament.name

class ReadPdfSerializer(BaseListCreateSerializer):
    file=serializers.FileField()
    

