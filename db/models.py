import sys
from django.db import models

class User(models.Model):
    tg_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=1024, null=True, blank=True)
    first_name = models.CharField(max_length=1024, null=True, blank=True)
    last_name = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = "users"

class Game(models.Model):
    group_id = models.IntegerField(null=True, blank=True)
    start_message_id = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(max_length=1024, null=True, blank=True)
    is_start = models.BooleanField(default=False)
    turn = models.IntegerField(null=True, blank=True)
    chamber_position = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "games"

class Usergame(models.Model):
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=1024, null=True, blank=True)
    turn_start_time = models.DateTimeField(max_length=1024, null=True, blank=True)
    is_pending = models.BooleanField(default=False)
    pending_message_id = models.IntegerField(null=True, blank=True)
    randfield = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "usergames"