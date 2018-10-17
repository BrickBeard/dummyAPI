from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class searchForm(forms.Form):
    search_query = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee ID, Name or Age'}), label='')


class create_form(forms.Form):
    name = forms.CharField(label='Name', max_length=50,
                           widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Employee Name'}))
    age = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Age'}))
    salary = forms.CharField(label='Salary', widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Salary'}))


class update_form(forms.Form):
    name = forms.CharField(label='Name', max_length=50,
                           widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Employee Name'}), required=False)
    age = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Age'}), required=False)
    salary = forms.CharField(label='Salary', widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Salary'}), required=False)


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
