from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView


from .forms import NoteForm
from .models import Note


class NoteList(ListView): #https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
    model = Note
    queryset = Note.objects.all()

    def get_queryset(self):
        folder = self.kwargs['folder']
        if folder == '':
            self.queryset = Note.objects.all()
            return self.queryset
        else:
            self.queryset = Note.objects.filter(folder__title__iexact=folder)
            return self.queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(NoteList, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        return context

class NoteDetail(DetailView):
    model = Note

class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm

class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('listall')

class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteForm
    
class NoteByTag(ListView):
    model = Note
    
    queryset = Note.objects.all()
    def get_queryset(self):
        tags = self.kwargs['tags']
        pieces = tags.split('/') #extract different tags separated by /
        
        queries = [Q(tag__title__iexact=value) for value in pieces]
        # Take one Q object from the list
        query = queries.pop()
        # Or the Q object with the ones remaining in the list
        for item in queries:
            query |= item
        # Query the model
        allnotes = Note.objects.filter(query).distinct().order_by('tag__title')
        self.queryset = allnotes #Setting the queryset to allow get_context_data to apply count
        return allnotes
    
    def get_context_data(self, **kwargs):
        context = super(NoteByTag, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        return context
