from django import forms

class MovieForm(forms.Form):
    game = forms.CharField(
        label='Search movie',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': 'only english title'})

    )