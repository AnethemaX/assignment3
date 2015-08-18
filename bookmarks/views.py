import re
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserProfile

from .forms import BookmarkForm, BookmarkFormUpdate
from .models import Bookmark
from django.core.serializers.json import DjangoJSONEncoder

class BookmarkList(ListView):
    model = Bookmark
    queryset = Bookmark.objects.all()
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookmarkList, self).dispatch(*args, **kwargs)

    
    def get_queryset(self):
        curruser = UserProfile.objects.get(user=self.request.user)
        folder = self.kwargs['folder']
        if folder == '':
            self.queryset = Bookmark.objects.filter(user=curruser)
            return self.queryset
        else:
            self.queryset = Bookmark.objects.all().filter(user=curruser).filter(folder__title__iexact=folder)
            return self.queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(BookmarkList, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class BookmarkDetail(DetailView):
    model = Bookmark
    
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    return super(BookmarkDetail, self).dispatch(*args, **kwargs)
        
    #def get_context_data(self, **kwargs):
    #    context = super(BookmarkDetail, self).get_context_data(**kwargs)
    #    context['curruser'] = UserProfile.objects.get(user=self.request.user)
    #    return context

    
class BookmarkCreate(CreateView):
    model = Bookmark
    form_class = BookmarkForm

class BookmarkDelete(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('listall')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookmarkDelete, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookmarkDelete, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context


class BookmarkUpdate(UpdateView):
    model = Bookmark
    form_class = BookmarkForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BookmarkUpdate, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(BookmarkUpdate, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context


class MyView(TemplateView):
    #setup the various forms in this view
    #folder_form_class = FolderForm
    #tag_form_class = TagForm
    bookmark_form_class = BookmarkForm
    template_name = "bookmarks/bookmark_hybrid.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyView, self).dispatch(*args, **kwargs)
    
    #called when loading the page for a new entry
    def get(self, request, *args, **kwargs):
        #setup all the forms by intialising the various form names with the corresponding form class
        #kwargs.setdefault("createfolder_form", self.folder_form_class())
        #kwargs.setdefault("createtag_form", self.tag_form_class())
        kwargs.setdefault("createbookmark_form", self.bookmark_form_class())
        kwargs.setdefault('curruser', UserProfile.objects.get(user=self.request.user))
        return super(MyView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_args = {
            'data': self.request.POST,
        }
        
        #if btn_createfolder hidden field is a value in POST form
        #if "btn_createfolder" in request.POST['form']: 
        #    form = self.folder_form_class(**form_args)
        #    #check if form is not value, reload the form with the POST values
        #    if not form.is_valid():
        #        #Construct the failed status (0) and the errors as message to be displayed in the template
        #        response_dict = {}
        #        response_dict['status'] = 0
        #        response_dict['message'] = form.errors.as_ul()
        #        return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
        #    else:
        #        #form is valid, save the form, and return all folders as data to update the folder select list
        #        form.save()
        #        data = Folder.objects.all()
        #        response_dict = {'status': 1}
        #        response_dict['message'] = list(data.values('id','title'))
        #       return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
        #if btn_createtag hidden field is a value in POST form
        #elif "btn_createtag" in request.POST['form']: 
        #    form = self.tag_form_class(**form_args)
        #    if not form.is_valid():
        #        #Construct the failed status (0) and the errors as message to be displayed in the template
        #        response_dict = {}
        #        response_dict['status'] = 0
        #        response_dict['message'] = form.errors.as_ul()
        #        return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
        #        #return self.get(request, createtag_form=form)
        #    else:
        #        #form is valid, save the form, and return all folders as data to update the tag multi-select list
        #        form.save() #save the new object
        #        data = Tag.objects.all() # retrieve all records
        #        response_dict = {'status': 1}
        #        response_dict['message'] = list(data.values('id','title'))
        #        return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.
        #if btn_createnote hidden field is a value in POST form
        #el
        if "btn_createbookmark" in request.POST['form']:
            form = self.bookmark_form_class(**form_args)
            if not form.is_valid():
                #Construct the failed status (0) and the errors as message to be displayed in the template
                #response_dict = {}
                #response_dict['status'] = 0
                #response_dict['message'] = form.errors.as_ul()
                #return HttpResponse(json.dumps(response_dict, cls=DjangoJSONEncoder))
                #return self.get(request, createnote_form=form, errors=response_dict) 
                return self.get(request,
                                   createbookmark_form=form) 
            else:
                try:
                    #Find out which user is logged in and get the correct UserProfile record.
                    curruser = UserProfile.objects.get(user=self.request.user)
                    obj = form.save(commit=False)
                    obj.user = curruser #Save the note note under that user
                    obj.save() #save the new object
                    
                except Exception, e:
                    print("errors" + str(e))
                    response = {'status': 1, 'message':'ok'}
                    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.

                #form is valid, save the form, and return all folders as data to update the tag multi-select list
                #form.save() #save the new object
                #response = {'status': 1, 'message':'Bookmark is created!'}
                #return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder)) #return to ajax as success with all the new records.
            
        return super(MyView, self).get(request)

#bookmark