from django import forms


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
