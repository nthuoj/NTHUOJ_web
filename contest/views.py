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

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

def index(request):
    
    problem1 = {'id':1,'name':'First Problem','ppl_pass':2,'ppl_not_pass':4}
    problem2 = {'id':2,'name':'Second Problem','ppl_pass':1,'ppl_not_pass':8}
    problem3 = {'id':3,'name':'third Problem','ppl_pass':5,'ppl_not_pass':1}
    problem_list = [problem1,problem2,problem3]

    ppl1 = {'name':'naruto'}
    ppl2 = {'name':'obama'}
    
    contestant_list = [ppl1,ppl2]

    ppl3 = {'name':'forest'}
    ppl4 = {'name':'gump'}

    coowner_list = [ppl3,ppl4]  

    contest1 = {'id':1,'name':'First contest','start_time':'2014/11/29 10:11:22','end_time':'2014/12/05 02:12:50',
                'contestant_number':200,'owner':'ma in joe','problem_list':problem_list,'contestant_list':contestant_list,
                'coowner_list':coowner_list}

    contest_list = [contest1]

    #contest_list = Contest.objects.order_by('-contest_id')
    #problem_list = Problem.objects.all()
    #contestant_list = {1:'naruto',2:'obama'}
    #coowner_list = {1:'teemo',2:'lux',3:'jinx'}
    return render(request, 'contest/index.html',{'contest_list':contest_list})

def contest(request,contest_id):

    problem1 = {'id':1,'name':'First Problem','ppl_pass':2,'ppl_not_pass':4}
    problem2 = {'id':2,'name':'Second Problem','ppl_pass':1,'ppl_not_pass':8}
    problem3 = {'id':3,'name':'third Problem','ppl_pass':5,'ppl_not_pass':1}
    problem_list = [problem1,problem2,problem3]

    ppl1 = {'name':'naruto','score':['0/3','1/2','1/4'],'solved':'2','panalty':'833'}
    ppl2 = {'name':'obama','score':['0/2','1/5','1/3'],'solved':'2','panalty':'83'}
    
    contestant_list = [ppl1,ppl2]

    clarification1 = {'id':1,'name':'First Problem','asker':'obama','content':'i have some problem','reply':'shut up'}

    clarification_list = [clarification1]

    contest1 = {'name':'First contest','start_time':'2014/11/29 10:11:22','end_time':'2014/12/05 02:12:50',
                    'contest_contestant':200,'contest_owner':'ma in joe','problem_list':problem_list,'contestant_list':contestant_list
                    ,'clarification_list':clarification_list}

    #contest_info = get_object_or_404(Contest,pk=contest_id)
    #problem_list = Problem.objects.order_by()
    #contestant_list = {1:{'name':'naruto','score':{1:'0/3',2:'1/2',3:'1/4'},'solved':'2','panalty':'833'},2:{'name':'obama','score':{1:'0/2',2:'1/5',3:'1/3'},'solved':'2','panalty':'83'}}
    return render(request, 'contest/contest.html',{'contest':contest1,'problem_list':problem_list,'contestant_list':contestant_list})

def navbar(request):
    return render(request, 'contest/navbar.html')
