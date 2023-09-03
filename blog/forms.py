from django import forms

from .models import Blog

from ckeditor.fields import RichTextField


class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)


class AddBlogForm(forms.ModelForm):
    description = RichTextField()
    
    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "banner",
            "description"
        )

class ReportForm(forms.Form):
    link = forms.URLField(label="Link")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Description")
