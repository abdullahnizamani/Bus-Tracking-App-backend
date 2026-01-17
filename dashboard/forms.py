from django import forms
from transport.models import Bus, Route
from users.models import Driver

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