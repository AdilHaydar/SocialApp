from django import forms
from .models import User, UserUpdateModel
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from phonenumber_field.formfields import PhoneNumberField

gender = (
    ('','Specify Gender'),
    ('Female','Female'),
    ('Male','Male')
)




class UserAdminCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email')

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
		fields = {'email','picture','admin','active'}

	def clean_password(self):
		return self.initial['password']

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label = 'Password Confirmation', widget= forms.PasswordInput)

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


class RegisterForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'email', 'picture','gender', 'name','surname', 'phone', 'password', 'confirm']

    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}

    picture = forms.ImageField(label = 'Picture', required=False)
    username = forms.CharField(label = 'Username')
    email = forms.EmailField(label="Email")
    gender = forms.ChoiceField(choices=gender,label="Gender")
    name = forms.CharField(label='Name', required=True)
    surname = forms.CharField(label='Surname', required=True)
    phone = forms.CharField(required=False, label="Phone")
    password = forms.CharField(label="Password",widget = forms.PasswordInput)
    confirm = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)
	

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        name = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')
        picture = self.cleaned_data.get('picture')
        gender = self.cleaned_data.get('gender')

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
        'picture':picture,
        'name':name,
        'surname':surname,
        'phone':phone,
        'gender':gender,
        }

        return values

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','name','gender','surname','phone','picture', 'password', 'confirm', 'admin']

    def __init__(self,*args,**kwargs):
        super(UserUpdateForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            if field == 'picture':
                continue
            self.fields[field].widget.attrs = {'class':'form-style', 'placeholder' : self.fields[field].label }

    picture = forms.ImageField(label = 'Picture', required=False)
    username = forms.CharField(label = 'Username')
    email = forms.EmailField(label = 'Email')
    name = forms.CharField(label='Name', required=True)
    surname = forms.CharField(label='Surname', required=True)
    phone = PhoneNumberField(required=False)
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput, required=False)
    confirm = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput, required=False)
    gender = forms.ChoiceField(choices=gender,label = 'Gender', required=False)
    admin = forms.BooleanField(label = 'Super User', required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        name = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')
        picture = self.cleaned_data.get('picture')
        gender = self.cleaned_data.get('gender')
        admin = self.cleaned_data.get('admin')

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
        'picture':picture,
        'name':name,
        'surname':surname,
        'phone':phone,
        'gender':gender,
        'admin':admin
        }

        return values
