from django import forms
from .models import Post, Comment, File, Tag


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['statement','location']

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['statement']

	def clean_statement(self):
		statement = self.cleaned_data['statement']
		if len(statement) == 0:
			raise forms.ValidationError("Comment cannot be left blank.")
		return statement

class FileForm(forms.ModelForm):

	class Meta:
		model = File
		fields = ['file']

	def __init__(self, *args, **kwargs):
		super(FileForm, self).__init__(*args,**kwargs)
		self.fields['file'].widget.attrs['multiple']

class TagForm:

	def clean_title(title):
		tag_model = Tag.objects.values_list('title', flat=True)
		#Tag.objects.values('title') yaptığımda sadece title değerlerini dict nesnesi olarak bana dönüyor
		#values_list 'i ise flat=True olmadan kullanırsam liste içerisinde her bir değeri tuple olarak veriyor.
		#values_list'i flat=True olarak kullanırsam tam istediğim gibi değerleri liste içerisinde veriyor.
		
		if title.startswith('#'):
			title = title.replace('#','',1)


		if title in tag_model:
			title = Tag.objects.get(title = title)
			return title
		else:
			new_tag = Tag()
			new_tag.title = title
			new_tag.save()
			return new_tag
