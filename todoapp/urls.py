from django import views
from django.urls import path
from . import views
from .views import TodoListView, AddTaskView, EditTaskView, DeleteTaskView, complete_task, logout_view

urlpatterns = [
    path('index', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.home_view, name='home'),
    path('todolist/', TodoListView.as_view(), name='todolist'),
    path('addtask/', AddTaskView.as_view(), name='addtask'),
    path('edittask/<int:task_id>/', EditTaskView.as_view(), name='edittask'),
    path('deletetask/<int:task_id>/', DeleteTaskView.as_view(), name='deletetask'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('logout/', logout_view, name='logout'),
    path('mail/', views.send_email, name='mail'),
]