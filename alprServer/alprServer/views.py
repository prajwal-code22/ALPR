from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app import models
from .utils import read_lp_from_image
import os
import cv2

@login_required
def home(request: HttpRequest):
    if request.method == "POST":
        long = request.POST.get("long")
        lat = request.POST.get("lat")
        uploaded_file = request.FILES.get("image") or request.FILES.get("video")

        file_type = uploaded_file.content_type.split("/")[0].lower()

        location, _ = models.Location.objects.get_or_create(long=long, lat=lat)

        scanned_plate = models.ScannedPlate(
            locaiont_id=location,
            user=request.user
        )
        scanned_plate.save()
        scanned_plate_id = scanned_plate.pk

        # Handle image here
        file_extension = uploaded_file.name.split('.')[-1].lower()
        file_name = f"{file_type}-{scanned_plate_id}-{request.user.pk}.{file_extension}"

        file_path = os.path.join(settings.LICENSE_PLATES, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        mat_img = cv2.imread(file_path)
        read_lp_from_image(scanned_plate_id ,mat_img)

        return render(request, "index.html", { "file_path":  file_path, "id": scanned_plate_id})

    return render(request, 'index.html')
