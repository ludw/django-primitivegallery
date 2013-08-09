from django import forms
from primitivegallery.models import Directory


def build_dir_choices():
    choices = []
    for item in Directory('').list():
        if not item['isfile']:
            choices.append((item['url'], item['name']))
    return choices


class UploadFileForm(forms.Form):
    directory = forms.ChoiceField(choices=build_dir_choices())
    files = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': 'multiple'}))
