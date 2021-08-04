from django.db import models


class Orgs(models.Model):
    org_name = models.CharField(max_length=90)
    org_guid = models.CharField(max_length=90)
    check_enabled = models.BooleanField(default=True)


class Spaces(models.Model):
    space_name = models.CharField(max_length=90)
    space_guid = models.CharField(max_length=90, unique=True)
    check_enabled = models.BooleanField(default=True)
    orgs = models.ForeignKey(Orgs, on_delete=models.CASCADE)


class Applications(models.Model):
    app_guid = models.CharField(max_length=90)
    app_name = models.CharField(max_length=90)
    spaces = models.ForeignKey(Spaces, on_delete=models.CASCADE)
    budget = models.IntegerField()
    budget_left = models.IntegerField()
    budget_reset_date = models.DateTimeField()
