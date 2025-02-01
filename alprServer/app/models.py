from django.db import models
from django.contrib.auth import get_user_model

class Location(models.Model):
    long = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

class ScannedPlate(models.Model):

    user = models.ForeignKey(get_user_model(), related_name="plates", on_delete=models.CASCADE, null=True, blank=True)
    locaiont_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="plates")
    scanned_at = models.DateTimeField(auto_now=True)
    plate = models.CharField(max_length=200, null=True, blank=True)
