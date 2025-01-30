

from django.http import HttpRequest
from django.shortcuts import render

def home(request: HttpRequest):

    if request.method == "POST":
        print("POSt request")

    return render(request, 'index.html')
