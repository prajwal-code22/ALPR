from django.db import models
from django.contrib.auth import get_user_model

class Location(models.Model):
    long = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

class ScannedPlate(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="plates", on_delete=models.CASCADE, null=True, blank=True)
    location_id= models.ForeignKey(Location, on_delete=models.CASCADE, related_name="plates")
    scanned_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='lp/')
    plate = models.CharField(max_length=200, null=True, blank=True)
    is_scanned = models.BooleanField(default=False)  # Track if a license plate has been associated

class LicensePlate(models.Model):
    scanned_plate = models.ForeignKey(ScannedPlate, on_delete=models.CASCADE, related_name="license_plates")
    plate_number = models.CharField(max_length=200, null=True, blank=True)
    plate_image = models.ImageField(upload_to='done/')
    state = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Update is_scanned field in ScannedPlate when a LicensePlate is added."""
        super().save(*args, **kwargs)
        self.scanned_plate.is_scanned = True
        self.scanned_plate.save()
