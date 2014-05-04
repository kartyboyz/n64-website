from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
import base64, json, urllib, hmac, time, hashlib
import uuid, os, datetime
import requests

import time

from n64.forms import BoxQueryForm, TextQueryForm, WatchForm 

def home(request):
    if request.user.is_authenticated():
        return render(request, 'base.html', {'logged_in':1})
    else:
        #show base home page
        return render(request, 'base.html', {'logged_in':0})

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    # Correct password, and the user is marked "active"
    if user is not None and user.is_active:
        auth.login(request, user)
        # Redirect to a success page.
        return render(request, 'base.html', {'logged_in':1})
    else:
        # Show an error page
        return render(request, 'base.html', {'logged_in':0, 'user_name': user})

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return render(request, 'base.html', {'logged_out':1})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, 'base.html', {'logged_in':1})
        else:
            return render(request, "create_user.html", {'form': form,})
    else:
        form = UserCreationForm()
        return render(request, "create_user.html", {'form': form,})

def query(request):
    if not request.user.is_authenticated():
        return redirect('home')

    ##ask for the query language API
    response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/query/info")
    query_api = response.json()
    
    if "reset_query" in request.POST:
        current_output = "count item"
        current_filter = "by finish"

    if "current_output" in request.POST:
        current_output = request.POST.get("current_output ")
    else:
        current_output = ""

    if "current_filter" in request.POST:
        current_filter = request.POST.get("current_filter")
    else:
        current_filter = ""

    ######TODO: format query_string from dropdown inputs, pass query_string as invisible field through form

    ##if we have a query, send query, wait for response
    if request.method == 'POST':
        form = TextQueryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ##-format new query string
            query_string = "%s : %s" % (cd['Output_text'], cd['Filter_text'])
            req_data = json.dumps({'query': query_string})
            ##-send GET to db
            response = requests.get('http://n64storageflask-env.elasticbeanstalk.com/query',
                    data=req_data, headers={'Content-Type': 'application/json'})
            ##-extract table from result
            query_result = response.json()
            return render(request, 'query.html', {'form': form, 'step_1': True, 'query_api': query_api, 'current_output': current_output,
                                                   'current_filter': current_filter, 'result_table': query_result,})
        else:
            if "output" in request.POST:
                my_output = request.POST.get("output")
                return render(request, 'query.html', {'form': form, 'step_2': True, 'output_set': True, 'current_output': current_output, 
                                                        'current_filter': current_filter, 'query_api': query_api})
            if "filter" in request.POST:
                my_filter = request.POST.get("filter")
                return render(request, 'query.html', {'form': form, 'step_2': True, 'filter_set': True, 'current_output': current_output, 
                                                        'current_filter': current_filter, 'query_api': query_api})

            if "submit_query" in request.POST:
                query_string = "%s : %s" % (outputs, char, courses, fields)
                req_data = json.dumps({'query': query_string})
                ##-send GET to db
                response = requests.get('http://n64storageflask-env.elasticbeanstalk.com/query',
                        data=req_data, headers={'Content-Type': 'application/json'})
                ##-extract table from result
                query_result = response.json()
                return render(request, 'query.html', {'form': form, 'step_1': True, 'query_api': query_api, 'current_output': current_output, 'current_filter': current_filter, 
                                                        'result_table': query_result})

    else:
        form = TextQueryForm()
    return render(request, 'query.html', {'form': form, 'step_1': True, 'query_api': query_api, 'current_output': current_output, 'current_filter': current_filter})

def watch(request):
    if not request.user.is_authenticated():
        return redirect('home')

    form = WatchForm()
    ##ask what videos we have access to
    user = request.user.username
    response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/users/%s/races" % user) 
    race_list = response.json()
    race_urls = []
    for race in race_list:
        race_urls.append(race['video_processed_url'])
    
    if request.method == 'GET' and 'video_id' in request.GET:
        #make list of race_urls
        race_list = response.json()
        race_urls = []
        for race in race_list:
            race_urls.append(race['video_processed_url'])
        ##make variables to pass to template
        video_num = int(request.GET['video_id'])
        video_url = race_urls[video_num]

        return render(request, 'watch.html', {'form': form, 'video_list': race_list, 'video_num': video_num, 'video_url': video_url})

    return render(request, 'watch.html', {'form': form, 'video_list': race_list})

def upload(request):
    if not request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        url = request.POST.get('video_url')
        session_data = json.dumps({'video_url': url, 'owner': request.user.username})
        #requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                #data=session_data, headers={'Content-Type': 'application/json'})
        return redirect('upload')

    return render(request, 'upload.html')

def sign_request(request):
    AWS_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET = os.environ['AWS_SECRET_KEY']
    S3_BUCKET = 'session-videos'

    uid = uuid.uuid1()
    ext = request.GET['s3_object_name'].split('.')[-1]
    object_name = 'raw/' + str(uid) + '.' + ext
    mime_type = request.GET['s3_object_type']
    expires = int(time.time() + 10)
    amz_headers = "x-amz-acl:public-read"
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET, put_request, hashlib.sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    resp = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ID, expires, signature),
        'url': url
    })
    return HttpResponse(resp, content_type='text/plain; charset=x-user-defined')

def races(request, session_id):
    if not request.user.is_authenticated():
        return redirect('home')

    user = request.user.username
    response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/sessions/%s" % session_id) 
    sess = response.json()
    if sess['owner'] != user:
        return redirect('sessions')
    response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/sessions/%s/races" % session_id) 
    races = response.json()
    initial_race = request.GET.get('video_id', None)
    initial_race = int(initial_race) if initial_race is not None else None
    race = races[initial_race-1] if initial_race is not None else None
    tags = None
    if race is not None:
        race_id = races[initial_race-1]['id']
        race['minutes'] = race['duration'] // 60
        race['seconds'] = int(race['duration']) % 60

        response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/tags/%s/%d" % (user, race_id)) 
        tags = response.json()

    return render(request, 'races.html', {'session':sess, 'race':race,
        'initial_race':initial_race, 'races':races, 'tags':tags})

def sessions(request):
    if not request.user.is_authenticated():
        return redirect('home')
    user = request.user.username
    response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/users/%s/sessions" % user) 
    user_sessions = response.json()
    for s in user_sessions: s['f_date'] = time.strptime(s['date'], '%a, %d %b %Y %H:%M:%S -0000')
    return render(request, 'sessions.html', {'sessions':user_sessions})

