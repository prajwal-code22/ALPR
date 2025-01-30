from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from app import models
from .plate_detector import detect_plate, r
import os
import json

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

        file_path = os.path.join(settings.LICENSE_PLATES, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        print(file_path)
        detect_plate(file_path, scanned_plate.pk, file_type)

        return render(request, "index.html", {"id": scanned_plate.pk, "file_path":  f"/media/lp/{file_name}" })

    return render(request, 'index.html')


def check_results(request: HttpRequest, id_):

    numbers = r.lrange(id_, 0, -1)

    if numbers is None:
        return render(request, "index.html", {"id": id_})
    
    sp = models.ScannedPlate.objects.get(pk=id_)

    ns = []
    for n in numbers:
        ns.extend(json.loads(n))

    sp.plate =  ",".join(ns)
    sp.save()


    return render(request, "index.html", {"id": id_, "numbers": ns})

