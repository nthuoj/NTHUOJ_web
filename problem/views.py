from django.shortcuts import render

# Create your views here.
def problem(request):
    a = {'name': 'my_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    b = {'name': 'all_problem', 'pid': 1, 'pass': 60, 'not_pass': 40}
    return render(request, 'problem/panel.html', {'my_problem':[a,a,a], 'all_problem':[a,a,a,b,b,b]})

def detail(request, problem_id):
    p = {
      'pid': 1,
      'description': 'this is a simple prblem',
      'input': 'input description',
      'output': 'output description',
      'samp_input': '1 2 3',
      'samp_output': 'A\nB\nC\n',
      'tag': ['dfs', 'bfs'],
      'testcase': [{'num': 1, 'time': 1, 'memory': 32}, {'num': 2, 'time': 3, 'memory': 100}],
    }
    return render(request, 'problem/detail.html', p)

def edit(request, problem_id):
    return render(request, 'problem/edit.html')

def new(request):
    return render(request, 'problem/edit.html')

def preview(request):
    return render(request, 'problem/preview.html')
