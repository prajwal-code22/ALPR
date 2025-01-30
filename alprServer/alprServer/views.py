from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from app import models
from .plate_detector import detect_plate
import os

def home(request: HttpRequest):

    if request.method == "POST":
        long = request.POST.get("long")
        lat = request.POST.get("lat")
        uploaded_file = request.FILES.get("image") or request.FILES.get("video")
        file_type = uploaded_file.content_type.split("/")[0]

        location, _ = models.Location.objects.get_or_create(long=long, lat=lat)
        scanned_plate = models.ScannedPlate(
            locaiont_id=location,
        )
        scanned_plate.save()

        # Handle image here
        file_extension = uploaded_file.name.split('.')[-1].lower()
        file_name = f"{file_type}-{scanned_plate.pk}-{request.user.pk}.{file_extension}"


        file_path = os.path.join(settings.TO_READ_FILE_PATH, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        detect_plate(file_path, scanned_plate.pk)

    return render(request, 'index.html')


# def check_results(request: HttpRequest):

#     id_ = 
