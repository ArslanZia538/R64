import datetime
from django.contrib.auth.models import User
from django.db import models


class Cash(models.Model):
    cash_id = models.AutoField(primary_key=True)
    reciever = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='cash_receiver')
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cash_giver')
    amount = models.IntegerField(blank=False, null=False)
    event = models.CharField(max_length=255, blank=False, null=False)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.reciever, self.giver, self.amount, self.event, self.date, self.status)


class History(models.Model):

    history_id = models.AutoField(primary_key=True)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_receiver')
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_giver')
    amount = models.IntegerField()
    event = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.reciever, self.giver, self.amount, self.event, self.date, self.status)