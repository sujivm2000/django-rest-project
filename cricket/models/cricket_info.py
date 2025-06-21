from base.models import BaseActiveModel
from django.db import models

# Choices for the role field
ROLE_CHOICES = [
    ('Batsman', 'Batsman'),
    ('Bowler', 'Bowler'),
    ('Allrounder', 'Allrounder'),
]


class Team(BaseActiveModel):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    coach = models.CharField(max_length=50)
    home_ground = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(BaseActiveModel):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False,
                             blank=False)  # Ensure 'Team' is defined elsewhere
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Batsman')
    batting_style = models.CharField(max_length=50, blank=True, null=True)
    bowling_style = models.CharField(max_length=50, blank=True, null=True)  # Corrected definition
    total_runs = models.IntegerField(default=0)  # Added default for numeric fields
    total_wickets = models.IntegerField(default=0)  # Added default for numeric fields

    class Meta(BaseActiveModel.Meta):
        verbose_name = 'Cricket Player'
        verbose_name_plural = 'Cricket Players'

    def __str__(self):
        return f'{self.name} ({self.team.name})'


class Tournament(BaseActiveModel):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.year}"



MATCH_TYPE_CHOICES = [
    ('ODI', 'ODI'),
    ('T20', 'T20'),
    ('TEST', 'TEST')
]


class Match(BaseActiveModel):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    date = models.DateField()
    venue = models.CharField(max_length=100)
    winner = models.ForeignKey(Team, related_name="won_matches", null=True, on_delete=models.SET_NULL)
    tournament = models.ForeignKey(Tournament, related_name='matches', null=True, blank=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.team1.name} v/s {self.team2.name}'


class ScoreCard(BaseActiveModel):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="scorecards")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="scores")
    runs = models.IntegerField()
    balls_faced = models.IntegerField()
    wickets = models.IntegerField(default=0)
    overs_bowled = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.player.name} - {self.match}"

