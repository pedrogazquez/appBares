from django import forms
from django.contrib.auth.models import User
from rango.models import Tapa, Bar, UserProfile

class BarForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Por favor introduzca el nombre del bar")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Bar

# class TapaForm(forms.ModelForm):
    # nombre = forms.CharField(max_length=128, help_text="Por favor introduzca el nombre de la tapa")
    # url = forms.URLField(max_length=200, help_text="Por favor introduzca la direccion de la imagen de la tapa")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # def clean(self):
        # cleaned_data = self.cleaned_data
        # url = cleaned_data.get('url')
        
        # # If url is not empty and doesn't start with 'http://' add 'http://' to the beginning
        # if url and not url.startswith('http://'):
            # url = 'http://' + url
            
            # cleaned_data['url'] = url
        # return cleaned_data

    # class Meta:
        # # Provide an association between the ModelForm and a model
        # model = Tapa

        # # What fields do we want to include in our form?
        # # This way we don't need every field in the model present.
        # # Some fields may allow NULL values, so we may not want to include them...
        # # Here, we are hiding the foreign keys
        # fields = ('nombre', 'url','views')

class TapaForm(forms.ModelForm):
	nombre = forms.CharField(max_length=128, help_text="Por favor introduzca el nombre de la tapa")
	url = forms.URLField(max_length=200, help_text="Por favor introduzca la direccion de la imagen de la tapa")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	class Meta:
		# Provide an association between the ModelForm and a model
		model = Tapa

		# What fields do we want to include in our form?
		# This way we don't need every field in the model present.
		# Some fields may allow NULL values, so we may not want to include them...
		# Here, we are hiding the foreign key.
		# we can either exclude the category field from the form,
		exclude = ('bar',)
		#or specify the fields to include (i.e. not include the category field)
		fields = ('nombre', 'url','views')
		
class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')