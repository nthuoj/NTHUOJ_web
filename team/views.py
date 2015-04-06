'''
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import random
import datetime
from utils.render_helper import render_index
from django.template import RequestContext
# Create your views here.

def team_list(request):
    team_profile = {
        'id': 1,
        'team_name': 'ISeaTeL',
        'leader': 'andy',
        'member': ['hydai', 'henry'],
        'description': 'we are ISeaTel',
        'create_time': datetime.datetime.now()
    }
    team_list = [{}]*200
    for i in range(200):  # Generate lots of entries for testing paging
        team_profile['id'] = i+1
        team_list[i] = team_profile.copy()

    paginator = Paginator(team_list, 25)  # Show 25 teams per page
    page = request.GET.get('page')

    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        teams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        teams = paginator.page(paginator.num_pages)

    return render_index(
        request,
        'team/teamList.html',
        {'team_list': teams})


def team_profile(request):
    piechart_data = []
    for l in ['WA', 'AC', 'RE', 'TLE', 'MLE', 'OLE', 'Others']:
        piechart_data += [{'label': l, 'data': random.randint(50, 100)}]
    team_stat = {
        'contest': ['icpc practice1', 'icpc practice2']
    }
    team_profile = {
        'id': 1,
        'team_name': 'ISeaTeL',
        'leader': 'andy',
        'member': ['hydai', 'henry'],
        'description': 'we are ISeaTel',
        'create_time': datetime.datetime.now()
    }

    return render_index(
        request,
        'team/teamProfile.html',
        {
            'piechart_data': json.dumps(piechart_data),
            'team_stat': team_stat,
            'team_profile': team_profile
        })
