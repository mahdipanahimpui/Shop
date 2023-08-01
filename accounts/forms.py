from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    pass1 = forms.CharField(label='password', widget=forms.PasswordInput)
    pass2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')


    def clean_pass2(self):
        # use clean_pass2 not clean pass1 because pass2 is not define in validation
        cd = self.cleaned_data
        pass1 = cd['pass1']
        pass2 = cd['pass2'] 

        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('passwords dont match')
        return pass2
    
    def save(self, commit=True): # commit comes from developer when called svas() method
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['pass1'])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField(
        help_text = 'you can change password using <a href="../password/">this form</a>.'
        )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']
    

    

