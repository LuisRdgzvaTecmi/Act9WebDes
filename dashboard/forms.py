from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'autocomplete': 'username',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'new-password',
        }),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        cpw = cleaned_data.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        }),
    )
