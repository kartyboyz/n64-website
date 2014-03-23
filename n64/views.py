from django.http import HttpResponse
from django.shortcuts import render
import datetime
from n64.forms import QueryForm

def home(request):
    return render(request, 'base.html')

def query(request):
    if request.method == 'post':
        form = QueryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ##do stuff with data
    else:
        form = QueryForm()
    return render(request, 'query.html', {'form': form})

def watch(request):
    return render(request, 'base.html')

def upload(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'base.html')

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
