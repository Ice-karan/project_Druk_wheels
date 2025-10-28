from django import forms 
from .models import Item

# CSS classes for styling form inputs
INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border dark:text-white dark:bg-gray-900'

# Choices for transmission field
TRANSMISSION_CHOICES = [
    ('', 'Select Transmission'),
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]

# Choices for fuel type field
FUEL_TYPE_CHOICES = [
    ('', 'Select Fuel Type'),
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric', 'Electric'),
    ('Hybrid', 'Hybrid'),
]

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'image', 'category', 'name', 'location', 'year', 
            'price', 'mileage', 'color', 'transmission', 'fuel_type', 
            'description'
        )

        # Define widgets for form fields to customize their appearance and behavior
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'year': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'mileage': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'color': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'transmission': forms.Select(attrs={'class': INPUT_CLASSES}, choices=TRANSMISSION_CHOICES),
            'fuel_type': forms.Select(attrs={'class': INPUT_CLASSES}, choices=FUEL_TYPE_CHOICES),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
        }

        # Label for empty selection in the category field
        empty_label = 'Select category'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set empty label for category field and initial value
        self.fields['category'].empty_label = 'Select category'
        self.fields['category'].initial = ''

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'is_sold', 'image', 'name', 'location', 'year', 
            'price', 'mileage', 'color', 'transmission', 'fuel_type', 
            'description'
        )

        # Define widgets for form fields to customize their appearance and behavior
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'year': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'mileage': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'color': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'transmission': forms.Select(attrs={'class': INPUT_CLASSES}, choices=TRANSMISSION_CHOICES),
            'fuel_type': forms.Select(attrs={'class': INPUT_CLASSES}, choices=FUEL_TYPE_CHOICES),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES}),
            'is_sold': forms.CheckboxInput(attrs={'class': 'text-left accent-emerald-500/25 w-5 h-5'}),
        }
