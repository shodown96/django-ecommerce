from django import forms
from .validators import validate_file_extension
from django.contrib.auth.models import User
from django.forms import ModelForm
from core.models import Address
# from ckeditor.widgets import CKEditorWidget


class ProfileForm(ModelForm):
    # phone_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = self.instance
        # user.profile.phone_number = self.cleaned_data['phone_number']
        user.profile.save()
        if commit:
            return super(ProfileForm, self).save()


# class NewsletterForm(forms.Form):
#     title = forms.CharField()
#     body = forms.CharField(widget=CKEditorWidget())


class PictureForm(forms.Form):
    picture = forms.ImageField(validators=[validate_file_extension])


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=(forms.PasswordInput()))
    remember = forms.CharField(widget=(forms.CheckboxInput))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
