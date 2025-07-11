from django.shortcuts import render, redirect
from django.http import JsonResponse


def landing(request):
    return render(request, 'landing.html')
