from django import forms


class idForm(forms.Form):
    id_form = forms.CharField(max_length=6, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee ID'}), label='')


class create_form(forms.Form):
    name = forms.CharField(label='Name', max_length=50,
                           widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Employee Name'}))
    age = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Age'}))
    salary = forms.CharField(label='Salary', widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Salary'}))


class update_form(forms.Form):
    name = forms.CharField(label='Name', max_length=50,
                           widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Employee Name'}))
    age = forms.CharField(label='Age', max_length=3, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Age'}))
    salary = forms.CharField(label='Salary', widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee Salary'}))
