from django.http import HttpResponse
from django.shortcuts import render

def index(request):
  return HttpResponse("Alpha store")

def test(request):
  return HttpResponse("Test route")
