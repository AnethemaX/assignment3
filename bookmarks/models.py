from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import UserProfile

# Create your models here.
class Bookmark(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.URLField()
    desc = models.TextField(null=True)
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk":self.pk})