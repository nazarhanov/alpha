from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

def index(request):
  return HttpResponse("Store frontend")

def status(request):
  if request.method == 'POST':
    return JsonResponse({'status': 'ok'})

  return redirect('/404')
