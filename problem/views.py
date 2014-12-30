from django.shortcuts import render

# Create your views here.
def problem(request):
    a = {'name': 'my_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    b = {'name': 'all_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    return render(request, 'problem/panel.html', {'my_problem':[a,a,a], 'all_problem':[a,a,a,b,b,b]})

def detail(request, problem_id):
    p = {
      'pid': problem_id,
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
