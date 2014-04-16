from django.http import HttpResponse
from django.shortcuts import render, redirect
import base64, json, urllib, hmac, time, hashlib
import uuid, os, datetime
import requests

from n64.forms import QueryForm, WatchForm 

def home(request):
    return render(request, 'base.html')

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
    ##ask what videos we have access to
    response = requests.get("http://n64storageflask-env.elasticbeanstalk.com/races") 
    race_list = response.json()
    race_urls = [race['video_url'] for race in race_list]
    
    if request.method == 'GET':
        form = WatchForm(request.GET)
        if form.is_valid():
            ##ask for your video url 
            cd = form.cleaned_data
            video_num = cd['videoNum']
            video_url = race_urls[video_num]
            return render(request, 'watch.html', {'form': form, 'video_list': race_urls, 'video_num': video_num, 'video_url': video_url})

    form = WatchForm()
    return render(request, 'watch.html', {'form': form, 'video_list': race_urls})

def upload(request):
    if request.method == 'POST':
        url = request.POST['video_url']
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

def sign_in(request):
    stuff = notdone
