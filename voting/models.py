from django.contrib.auth.models import User
from django.db.models import *
from django.db import models
from users.models import Profile


class Candidate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='candidate_pics')
    
    def __str__(self):
        return self.name

class VotingSession(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    active = models.BooleanField(default=True)
    year = models.IntegerField()
    university = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to='voting_pics', null=False, blank=False)
    candidates = models.ManyToManyField('Candidate', related_name='candidates')

    def __str__(self):
        return self.name



class VoteUser(Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    voting_session = models.ForeignKey('VotingSession', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"VoteUser: {self.user.username}"
