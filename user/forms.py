from django import forms
from .models import User, UserUpdateModel
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm


class UserAdminCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email', 'birthday')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserAdminChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = {'email','avatar','birthday','admin','active','is_banned'}

	def clean_password(self):
		return self.initial['password']

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label = 'Password Confirmation', widget= forms.PasswordInput)
	birthday = forms.DateField(label = 'Birthday', widget=forms.DateInput(attrs={'type':'date'}))

	class Meta:
		model = User
		fields = ['username']

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.clean_data['password1'])
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	username = forms.CharField(label = 'Username')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		fields = ['username','password']

	def __init__(self,*args,**kwargs):
		super(LoginForm, self).__init__(*args,**kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs = {'class':'login-inputs'}


class RegisterForm(forms.Form):
	class Meta:
		model = User
		fields = ['username', 'email','info','web_page','avatar', 'birthday', 'password', 'confirm']

	def __init__(self,*args,**kwargs):
		super(RegisterForm, self).__init__(*args,**kwargs)
		for field in self.fields:
			if field == 'avatar':
				self.fields[field].widget.attrs = {'onchange':'readAvatar(this)','accept':".jpg, .jpeg, .png, .mp4, .wmv, .avi"}
				continue
			self.fields[field].widget.attrs = {'class':'form-control'}

	avatar = forms.ImageField(label = 'Avatar', required=False)
	username = forms.CharField(label = 'Username')
	email = forms.EmailField()
	info = forms.CharField(label = 'User Info', required = False, widget=forms.Textarea(attrs={'id':'id_statement','rows':'2'}))
	web_page = forms.URLField(label = 'Web Page', required=False)
	birthday = forms.DateField(label = 'Birthday', widget=forms.DateInput(attrs={'type':'date'}), required=False)
	password = forms.CharField(widget = forms.PasswordInput)
	confirm = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)
	

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		confirm = self.cleaned_data.get('confirm')
		email = self.cleaned_data.get('email')
		avatar = self.cleaned_data.get('avatar')
		birthday = self.cleaned_data.get('birthday')
		info = self.cleaned_data.get('info')
		web_page = self.cleaned_data.get('web_page')

		if password and confirm and password != confirm:
			raise forms.ValidationError("Passwords doesn't match")
		if email == False:
			raise forms.ValidationError("A valid Email Address")
		if len(username) < 3:
			raise forms.ValidationError("Username (%s) is can't be less than 6 characters." %username)

		values = {
		'username' : username,
		'password' : password,
		'email' : email,
		'avatar': avatar,
		'birthday' : birthday,
		'info' : info,
		'web_page' : web_page,
		}

		return values

class UserUpdateForm(forms.ModelForm):
    
	class Meta:
		model = User
		fields = ['username', 'email','info','web_page','avatar', 'birthday', 'password', 'confirm']

	def __init__(self,*args,**kwargs):
		super(UserUpdateForm, self).__init__(*args,**kwargs)
		for field in self.fields:
			if field == 'avatar':
				self.fields[field].widget.attrs = {'onchange':'readAvatar(this)','accept':".jpg, .jpeg, .png, .mp4, .wmv, .avi"}
				continue
			self.fields[field].widget.attrs = {'class':'form-control'}

	avatar = forms.ImageField(label = 'Avatar', required=False)
	username = forms.CharField(label = 'Username')
	email = forms.EmailField()
	info = forms.CharField(label = 'User Info', required = False, widget=forms.Textarea(attrs={'rows':'5'}))
	web_page = forms.URLField(label = 'Web Page', required=False)
	birthday = forms.DateField(label = 'Birthday', widget=forms.DateInput(attrs={'type':'date'}), required=False)
	password = forms.CharField(widget = forms.PasswordInput)
	confirm = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		confirm = self.cleaned_data.get('confirm')
		email = self.cleaned_data.get('email')
		avatar = self.cleaned_data.get('avatar')
		birthday = self.cleaned_data.get('birthday')
		info = self.cleaned_data.get('info')
		web_page = self.cleaned_data.get('web_page')
		

		if password and confirm and password != confirm:
			raise forms.ValidationError("Passwords doesn't match")
		if email == False:
			raise forms.ValidationError("A valid Email Address")

		values = {
		'username' : username,
		'password' : password,
		'email' : email,
		'avatar': avatar,
		'birthday' : birthday,
		'info' : info,
		'web_page' : web_page,
		}

		return values