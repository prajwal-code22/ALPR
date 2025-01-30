from django.db import models

class Location(models.Model):
    long = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

class ScannedPlate(models.Model):

    locaiont_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="plates")
    scanned_at = models.DateTimeField(auto_now=True)
    plate = models.CharField(max_length=200, null=True, blank=True)
