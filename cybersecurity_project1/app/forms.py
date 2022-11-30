from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

def image_validator(value):
    try:
        from PIL import Image
    except ImportError:
        return []
    else:
        try:
            im = Image.open(value.file)
            im.verify()
        except:
            raise ValidationError("File is not valid image")
class SizeValidator(object):
    def __init__(self, size) -> None:
        self.size = size
    def __call__(self, value):
        if value.size > self.size:
            raise ValidationError("File is too large")
        return []
class CustomFilesFiled(forms.FileField):
    default_validators = [
        validators.validate_image_file_extension,
        SizeValidator(10*10**6), # 10MB
        image_validator
    ]

class PostForm(forms.Form):
    content = forms.CharField(
        label = "What do you want to share with your friends?",
        max_length = 500,
        required = False
    )
    public = forms.BooleanField(
        label = "Is this public for anyone to see?",
        required = False
    )
    attachment = CustomFilesFiled(
        widget = forms.ClearableFileInput(attrs = {'multiple': True}),
        required = False
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_content = cleaned_data.get("content")
        cleaned_attachment = cleaned_data.get("attachment")
        if not cleaned_content and not cleaned_attachment:
            raise forms.ValidationError("No text nor attachments!")
