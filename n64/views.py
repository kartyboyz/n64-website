from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
import base64, json, urllib, hmac, time, hashlib
import uuid, os, datetime
import requests

from n64.forms import QueryForm, WatchForm 

def home(request):
    return render(request, 'base.html')

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
    ##if we have a query, send query, wait for response
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ##-format new query string
            query_string = "%s : %s" % (cd['Outputs'], cd['Filters'])
            req_data = json.dumps({'query': query_string})

            ##-send GET to db
            response = requests.get('http://n64storageflask-env.elasticbeanstalk.com/query',
                    data=req_data, headers={'Content-Type': 'application/json'})
            ##-extract table from result
            query_result = response.json()
        return render(request, 'query.html', {'form': form, 'result_table': query_result, 'test': True})

    else:
        form = QueryForm()
    return render(request, 'query.html', {'form': form})

def watch(request):
    form = WatchForm()
    ##ask what videos we have access to
    user = 'mgabed'
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
    if request.method == 'POST':
        url = request.POST.get('video_url')
        session_data = json.dumps({'video_url': url})
        requests.post('http://n64storageflask-env.elasticbeanstalk.com/sessions',
                data=session_data, headers={'Content-Type': 'application/json'})
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
