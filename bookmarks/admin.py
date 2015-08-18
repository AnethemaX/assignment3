from django.contrib import admin
from .models import Bookmark
from accounts.models import UserProfile

# Register your models here.
admin.site.register(Bookmark)
admin.site.register(UserProfile)