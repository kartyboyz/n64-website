from django.http import HttpResponse
from django.shortcuts import render
import base64, json, urllib, hmac, time, hashlib
import uuid, os, datetime

from n64.forms import QueryForm

def home(request):
    return render(request, 'base.html')

def query(request):
    ##if we have a query, send query, wait for response
    if request.method == 'post':
        form = QueryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ##new query post to db
            query_string = cd['query']
            query = json.dumps({'query': query_string})
            requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                    data=query_string, headers={'Content-Type': 'application/json'})
        return render(request, 'query.html', {'form': form, 'result': result})

    else:
        form = QueryForm()
    return render(request, 'query.html', {'form': form})

def watch(request):
    if request.method == 'get':
        form = WatchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            ##ask for your video  
            ##video_num = cd['video']
            ##video = json.dumps({'video': video_num})
            ##requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
            ##        data=video, headers={'Content-Type': 'application/json'})
            ##return render(request, 'watch.html', {'form': form, 'video': video})
    else:
        return render(request, 'watch.html', {'form': form})

def upload(request):
    if request.method == 'POST':
        url = request.POST['video_url']
        session_data = json.dumps({'video_url': url})
        requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                data=session_data, headers={'Content-Type': 'application/json'})
        return redirect('upload')

    return render(request, 'upload.html')
