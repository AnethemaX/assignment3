from django import forms
from .models import Bookmark
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button

class BookmarkForm(forms.ModelForm):
    class Meta: 
        model = Bookmark
        
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Save', 'Save', css_class='btn-primary'))
    #helper.form_class = 'form_horizontal'
    #helper.label_class = "col-sm-4"
    #helper.field_class = "col-sm-8"