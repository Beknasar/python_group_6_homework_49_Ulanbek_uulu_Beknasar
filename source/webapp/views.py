from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Tasks
from django.views.generic import View, TemplateView

from django.http import HttpResponseNotAllowed
from .forms import TaskForm

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tasks']=Tasks.objects.all()
        return context


class TaskView(TemplateView):
    template_name = 'task_view.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        context['task'] = task
        return context

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_create.html', context={
            'form': form
        })
    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = Tasks.objects.create(
                summary=form.cleaned_data['summary'],
                description = form.cleaned_data['description'],
                type = form.cleaned_data['type'],
                status = form.cleaned_data['status'],)

            return redirect('task_view', pk=task.pk)
        else:
            return render(request, 'task_create.html', context={
                'form': form
            })

class UpdateView(TemplateView):
    template_name = 'task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)
        form = TaskForm(initial={
            'summary': task.summary,
            'description': task.description,
            'type': task.type,
            'status': task.status
        })
        context['task'] = task
        context['form'] = form
        return context

    def post(self, request, pk):
       form = TaskForm(data=request.POST)
       task = get_object_or_404(Tasks, pk=pk)
       if form.is_valid():
            task.summary = form.cleaned_data['summary']
            task.description = form.cleaned_data['description']
            task.status = form.cleaned_data['status']
            task.type = form.cleaned_data['type']
            task.save()
            return redirect('task_view', pk=task.pk)
       else:
            return self.render_to_response(context={
                'task': task,
                'form': form
            })


class DeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)
        return render(request, 'task_delete.html', context={'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Tasks, pk=pk)
        task.delete()
        return redirect('index')

# class DeleteView(TemplateView):
#     template_name = 'task_delete.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         task = get_object_or_404(Tasks, pk=pk)
#         context['task'] = task
#         return context
#
#     def post(self, request, pk):
#         task = get_object_or_404(Tasks, pk=pk)
#         task.delete()
#         return redirect('index')