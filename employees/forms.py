from django import forms


class idForm(forms.Form):
    id_form = forms.CharField(max_length=6, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Employee ID'}), label='')
