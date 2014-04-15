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
            response = requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                    data=query_string, headers={'Content-Type': 'application/json'})
            result = json.loads(response.text)
        return render(request, 'query.html', {'form': form, 'result': result})

    else:
        form = QueryForm()
    return render(request, 'query.html', {'form': form})

def watch(request):
    form = WatchForm(request.GET)
    ##ask what videos we have access to
    user_info = json.dumps({'user': user.username})
    response = requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
            data=user_info, headers={'Content-Type': 'application/json'})
    video_list = json.loads(response.text)

    if request.method == 'get':
        if form.is_valid():
            ##ask for your video url 
            cd = form.cleaned_data
            video_num = cd['video']
            video = json.dumps({'video': video_num})
            response = requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                    data=video, headers={'Content-Type': 'application/json'})
            result = json.loads(response.text)
            return render(request, 'watch.html', {'form': form, 'video_list': video_list, 'video': result})

    return render(request, 'watch.html', {'form': form, 'video_list': video_list})

def upload(request):
    if request.method == 'POST':
        url = request.POST['video_url']
        session_data = json.dumps({'video_url': url})
        requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                data=session_data, headers={'Content-Type': 'application/json'})
        return redirect('upload')

    return render(request, 'upload.html')
