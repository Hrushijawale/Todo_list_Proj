
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from . import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import UserSignIn
from django.views import View
from .models import TodoTask
from django.core.mail import send_mail
from django.contrib import messages
from .models import TodoTask, UserProfile
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, redirect
from .models import UserProfile
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth import logout
from .models import UserProfile
from .models import TodoTask



def index(request):
    return HttpResponse("This is from index")

def home(request):
    return render(request, 'todoapp/home.html')

def todo_list(request):
    return render(request, 'todoapp/todolist.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_signin = UserSignIn.objects.get(username=username, password=password)
        except UserSignIn.DoesNotExist:
            messages.warning(request, 'Account not found. Please sign up.')
            return redirect('home') 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'todoapp/login.html')  


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        age = request.POST['age']

        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        
        new_user_profile = UserProfile(
            name=name,
            email=email,
            password=password,
            phone_number=phone_number,
            age=age
        )
        new_user_profile.save()

        return redirect('login')  
    else:
        return render(request, 'todoapp/signup.html')



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the home page after logout


class TodoListView(View):
    template_name = 'todoapp/todolist.html'

    def get(self, request):
        tasks = TodoTask.objects.all()
        return render(request, self.template_name, {'tasks': tasks})
    

def todo_list(request):
    tasks = TodoTask.objects.all()
    incomplete_tasks_count = TodoTask.objects.filter(completed=False).count()
    return render(request, 'todo_list.html', {'tasks': tasks, 'incomplete_tasks_count': incomplete_tasks_count})


class AddTaskView(View):
    template_name = 'todoapp/addtask.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        finish_time = request.POST.get('finish_time')

        try:
            finish_time = timezone.datetime.strptime(finish_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            messages.error(request, 'Invalid date and time format. Please use YYYY-MM-DDTHH:MM.')
            return redirect('addtask')

        TodoTask.objects.create(title=title, description=description, finish_time=finish_time)
        messages.success(request, 'Task added successfully.')
        return redirect('todolist')

class EditTaskView(View):
    template_name = 'todoapp/edittask.html'

    def get(self, request, task_id):
        task = TodoTask.objects.get(id=task_id)
        return render(request, self.template_name, {'task': task})

    def post(self, request, task_id):
        task = TodoTask.objects.get(id=task_id)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.finish_time = timezone.datetime.strptime(request.POST.get('finish_time'), '%Y-%m-%dT%H:%M')
        task.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('todolist')



class DeleteTaskView(View):
    template_name = 'todoapp/deletetask.html'

    def get(self, request, task_id):
        task = TodoTask.objects.get(id=task_id)
        return render(request, self.template_name, {'task': task})

    def post(self, request, task_id):
        action = request.POST.get('action')

        if action == 'delete':
            task = TodoTask.objects.get(id=task_id)
            task.delete()
            messages.success(request, 'Task deleted successfully.')
    

        return redirect('todolist')
    
   
# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.http import HttpResponse
# from .models import TodoTask

# def complete_task(request, task_id):
   
#     task = get_object_or_404(TodoTask, pk=task_id)
#     task.completed = not task.completed
#     task.save()
#     response_data = {'status': 'success', 'title': task.title, 'completed': task.completed} 
#     return HttpResponse(content_type='application/json', content=response_data)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TodoTask

# def complete_task(request, task_id):
#     task = get_object_or_404(TodoTask, pk=task_id)
#     task.completed = not task.completed
#     task.save()

#     # Calculate the number of incomplete tasks
#     incomplete_tasks_count = TodoTask.objects.filter(completed=False).count()

#     # Prepare the data to send back as JSON response
#     response_data = {
#         'status': 'success',
#         'title': task.title,
#         'completed': task.completed,
#         'incomplete_tasks_count': incomplete_tasks_count  # Pass the number of incomplete tasks
#     }
    
#     # Return JSON response with the updated data
#     return JsonResponse(response_data)

from django.http import JsonResponse

def complete_task(request, task_id):
    task = get_object_or_404(TodoTask, pk=task_id)
    task.completed = not task.completed
    task.save()

    response_data = {
        'status': 'success',
        'completed': task.completed,
    }
    return JsonResponse(response_data)


from django.shortcuts import render
from .models import TodoTask

def incomplete_tasks_view(request):
    all_tasks = TodoTask.objects.all()

    completed_tasks_count = TodoTask.objects.filter(completed=True).count()
    
    incomplete_tasks_count = all_tasks.count() - completed_tasks_count
    
    incomplete_tasks = all_tasks.filter(completed=False)
    
    return render(request, 'todoapp/todolist.html', {
        'incomplete_tasks': incomplete_tasks,
        'incomplete_tasks_count': incomplete_tasks_count
    })