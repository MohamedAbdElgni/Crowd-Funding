from django import forms
from .models import *
from taggit.forms import TagField

class ProjectForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'tags']
        widgets = {
            'start_time': forms.DateInput(attrs={"class": "form-control w-50 ",'type': 'date'}),
            'end_time': forms.DateInput(attrs={"class": "form-control w-50",'type': 'date'}),
            'title':forms.TextInput(attrs={"class": "form-control w-100 ","placeholder":"Enter title"}),
            'details':forms.Textarea(attrs={"class": "form-control w-100  ","placeholder":"Enter title", "rows": "5"}),
            'category':forms.Select(attrs={"class": "form-control  w-50"}),
            'total_target':forms.TextInput(attrs={"class": "form-control w-50","placeholder":"ex.2000"}),
            'tags':forms.TextInput(attrs={"class": "form-control w-50","placeholder":"ex.2000"}),
       
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            return [tag.strip() for tag in tags.split(',')]
        return []
    
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImageForm(forms.ModelForm):
    image = MultipleFileField(label='Images', required=False)

    class Meta:
        model = ProjectPicture
        fields = ("image",)


    