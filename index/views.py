from django.shortcuts import render
from django.http import HttpResponse
import time
import datetime
# Create your views here.
def home(request):
	t = time.time()
    	tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
	return render(request, 'newindex.html', { 'tstr':tstr, 'info1':123, 'info2':123456789, 'Column_content':'Column content', 'contest1':'DS', 'contest2':'junior', 'contest3':'senior', 'contest4':'ABCDEFG', 'contest5':'GGGGGG', 'rtime1':'100 days', 'rtime2':'1 seconds', 'rtime3':'0 seconds', 'utime1':'?????', 'utime2':'@@', 'people':'123' })

def base(request):
	t = time.time()
    	tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
	return render(request, 'base.html', { 'tstr':tstr, 'info1':123, 'info2':123456789, 'people':'123' })

def broken(request):
	return render(request, 'brokenpage.html', {'error_message':'error message', 'people':'123'})

def get_time(request):
	t = time.time()
    	tstr = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
	return HttpResponse(tstr)

def submit(request):
	return render(request, 'submit.html', {'people':'123'})

def status(request):
	return render(request, 'status.html', {'people':'123'})

def group_list(request):
	return render(request, 'group_list.html', {'people':'123'})

def team_list(request):
	return render(request, 'team_list.html', {'people':'123'})
