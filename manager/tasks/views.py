# tasks/views.py
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Task

class TaskListView(View):
    template_name = 'tasks/tasks_list.html'

    def get(self, request):
        tasks = Task.objects.all()
        return render(request, self.template_name, {'tasks': tasks})
