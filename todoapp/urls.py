from django import views
from django.urls import path
from . import views
from .views import TodoListView, AddTaskView, EditTaskView, DeleteTaskView, complete_task

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    #path('todolist/', views.create_todo_list, name='todolist'),
    path('todolist/', TodoListView.as_view(), name='todolist'),
    path('addtask/', AddTaskView.as_view(), name='addtask'),
    path('edittask/<int:task_id>/', EditTaskView.as_view(), name='edittask'),
    path('deletetask/<int:task_id>/', DeleteTaskView.as_view(), name='deletetask'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    # path('notification/<int:task_id>/', NotificationView.as_view(), name='notification'),
    # Add other URL patterns as needed
]