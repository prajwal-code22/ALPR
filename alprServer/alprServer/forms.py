from django import forms


class UploadFileForm(forms.Form):
    image = forms.FileField(required=False)
    video = forms.FileField(required=False)