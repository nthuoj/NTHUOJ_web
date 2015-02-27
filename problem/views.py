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
from problem.models import Problem

# Create your views here.
def problem(request):
    a = {'name': 'my_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    b = {'name': 'all_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    return render(request, 'problem/panel.html', {'my_problem':[a,a,a], 'all_problem':[a,a,a,b,b,b]})

def volume(request):
    problem_id=[]
    if Problem.objects.count() != 0:
        problems = Problem.objects.latest('id')
        volume_number = (problems.id - 1) // 100
        for i in range(1,volume_number + 2):
            start_id = ((i - 1) * 100 + 1)
            if problems.id < i * 100:
                end_id = problems.id
            else:
                end_id = i * 100
            problem_id.append(str(start_id) + ' ~ ' + str(end_id))

    return render(request, 'problem/volume.html', {'problem_id':problem_id})

def detail(request, problem_id):
    p = {
      'pid': problem_id,
      'title': 'A a+b problem',
      'description': 'Given a, b, output a+b.',
      'input': 'a, b <= 100000000',
      'output': 'a+b',
      'samp_input': '1 2\n4 5',
      'samp_output': '3\n9\n',
      'tag': [''],
      'testcase': [{'num': 1, 'time': 1, 'memory': 32}, {'num': 2, 'time': 3, 'memory': 100}],
    }
    return render(request, 'problem/detail.html', p)

def edit(request, problem_id):
    return render(request, 'problem/edit.html')

def new(request):
    return render(request, 'problem/edit.html')

def preview(request):
    return render(request, 'problem/preview.html')
