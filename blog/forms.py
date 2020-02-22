from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class AnotherForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    content = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Post
        fields = ['title', 'content']

class UpdateBlogPostForm(forms.ModelForm):
	class Meta:
		model = Post
		widgets = {
            #'foo': SummernoteWidget(),
            'content': SummernoteWidget(),
        }
		fields = ['title', 'content']
		#content = forms.CharField(widget=SummernoteWidget())
	def save(self, commit=True):
		post = self.instance
		post.title = self.cleaned_data['title']
		post.content = self.cleaned_data['content']


		if commit:
			post.save()
		return post

