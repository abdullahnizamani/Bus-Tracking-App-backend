from django import forms
from transport.models import Bus, Route
from users.models import Driver, User
from django.core.exceptions import ValidationError
class BusForm(forms.ModelForm):
    
    class Meta:
        model = Bus
        fields = ['name', 'registration_number', 'driver', 'capacity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Enter bus name'}),
            'registration_number': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Enter registration number'}),
            'driver': forms.Select(attrs={'class': 'select select-bordered w-full'}),
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



class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'username']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full pl-10',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full pl-10',
                'placeholder': 'Last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full pl-10',
                'placeholder': 'user@example.com',
            }),
            'username': forms.TextInput(attrs={
                'class': 'input input-ghost w-full join-item focus:bg-transparent focus:outline-none',
                'placeholder': 'Username',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full pl-10',
                'placeholder': '+92 3XX XXXXXXX',
            }),
            # 'avatar': forms.FileInput(attrs={
            #     'class': 'absolute inset-0 opacity-0 cursor-pointer',
            #     'placeholder':''
            # }),
            'avatar': forms.FileInput(attrs={
                'class': 'absolute inset-0 opacity-0 cursor-pointer',
                'id': 'avatarInput',
                'accept': 'image/*'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise ValidationError("This Email is already taken. Please choose another.")
        return email