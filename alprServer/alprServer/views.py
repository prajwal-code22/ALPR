

from django.http import HttpRequest
from django.shortcuts import render

def home(request: HttpRequest):

    if request.method == "POST":
        # Handle image here
        file = request.FILES.get("image")
        print(file)


    return render(request, 'index.html')
