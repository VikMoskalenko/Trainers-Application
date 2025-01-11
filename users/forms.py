from django import forms
from users.models import User as CustomUser
class loginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class registerForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
    def save(self, commit=True):
        #user = super().save(self.cleaned_data["password"])
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user