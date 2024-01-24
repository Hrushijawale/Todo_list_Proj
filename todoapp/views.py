
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
# User = settings.AUTH_USER_MODEL
from .models import UserSignIn
from django.views import View
from .models import TodoTask
from django.core.mail import send_mail
from django.contrib import messages
from .models import TodoTask, UserProfile
from .models import *
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.contrib.auth.models import User

# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile
from django.conf import settings
User = settings.AUTH_USER_MODEL



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

        # Check if login credentials exist in the UserSignIn model
        try:
            user_signin = UserSignIn.objects.get(username=username, password=password)
        except UserSignIn.DoesNotExist:
            messages.warning(request, 'Account not found. Please sign up.')
            return redirect('home') 

        # Authenticate user against the custom User model
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
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')

        # Create a new user
        user = User.objects.create_user(username=email, email=email, password=password)

        # Create a user profile with the additional fields
        user_profile = UserProfile.objects.create(
            user=user,
            name=name,
            email=email,
            password=password,
            phone_number=phone_number,
            age=age,
        )

        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login') 

    return render(request, 'todoapp/signup.html')


# @login_required
class TodoListView(View):
    template_name = 'todoapp/todolist.html'

    def get(self, request):
        tasks = TodoTask.objects.all()
        return render(request, self.template_name, {'tasks': tasks})

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

# views.py

# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib import messages
# from .models import TodoTask

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
        # If 'Cancel' or an unknown action, do nothing

        return redirect('todolist')
    
    # views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import TodoTask

def complete_task(request, task_id):
    # Get the task object from the database
    task = get_object_or_404(TodoTask, pk=task_id)

    # Toggle the 'completed' status
    task.completed = not task.completed

    # Save the updated task
    task.save()

    # Return a JSON response indicating success
    response_data = {'status': 'success', 'title': task.title, 'completed': task.completed}
    
    # If you prefer to use JsonResponse
    # return JsonResponse(response_data)

    # If you prefer to use HttpResponse
    return HttpResponse(content_type='application/json', content=response_data)
