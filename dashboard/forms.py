from django import forms
from transport.models import Bus, Route
from users.models import Driver, User

class BusForm(forms.ModelForm):
    
    class Meta:
        model = Bus
        fields = ['name', 'registration_number', 'driver_id', 'capacity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Enter bus name'}),
            'registration_number': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Enter registration number'}),
            'driver_id': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'capacity': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Enter capacity'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered focus:input-primary w-full',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered focus:input-primary w-full',
                'placeholder': 'Last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered focus:input-primary w-full',
                'placeholder': 'user@example.com',
            }),
            'username': forms.TextInput(attrs={
                'class': 'input input-bordered focus:input-primary w-full',
                'placeholder': 'Username',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered focus:input-primary w-full',
                'placeholder': '+92 3XX XXXXXXX',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'file-input file-input-bordered file-input-primary w-full',
            }),
        }