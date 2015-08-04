from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookmark
from django.core.urlresolvers import reverse

# Create your views here.
def bookmark_list(request):
    allbookmarks = Bookmark.objects.all()
    return render(request, 'bookmarks/index.html', {'bookmarks': allbookmarks})   


#def bookmark_detail(request, bookmark_id):
#    bookmark = Bookmark.objects.get(id=bookmark_id)
#    responsetext = ""
#    responsetext += "<h1>" + str(bookmark.id) + "</h1>"
#    responsetext += "<h2>" + bookmark.title + "</h2>"
#    responsetext += "<a href='" + bookmark.content + "'" + "<h2>" + bookmark.content + "</h2>" + "</a>"
#    return HttpResponse(responsetext)

def bookmark_detail(request, bookmark_id):
    bookmark = Bookmark.objects.get(id=bookmark_id)
    return render(request, 'bookmarks/specific.html', {'bookmarks': bookmark})   