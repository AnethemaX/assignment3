from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import BookmarkForm
from .models import Bookmark

class BookmarkList(ListView):
    model = Bookmark
    queryset = Bookmark.objects.all()
    
    def get_queryset(self):
        folder = self.kwargs['folder']
        if folder == '':
            self.queryset = Bookmark.objects.all()
            return self.queryset
        else:
            self.queryset = Bookmark.objects.filter(folder__title__iexact=folder)
            return self.queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(BookmarkList, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        return context

class BookmarkDetail(DetailView):
    model = Bookmark
    
class BookmarkCreate(CreateView):
    model = Bookmark
    form_class = BookmarkForm

class BookmarkDelete(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('listall')

class BookmarkUpdate(UpdateView):
    model = Bookmark
    form_class = BookmarkForm
    