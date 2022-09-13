from django import forms

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
    attachment = forms.FileField(
        widget = forms.ClearableFileInput(attrs = {'multiple': True}),
        required = False
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_content = cleaned_data.get("content")
        cleaned_attachment = cleaned_data.get("attachment")
        if not cleaned_content and not cleaned_attachment:
            raise forms.ValidationError("No text nor attachments!")
