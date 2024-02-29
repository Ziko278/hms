from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, TextInput, RadioSelect, CheckboxInput, CheckboxSelectMultiple, DateInput
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from pharmacy.models import *


class DrugCategoryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugCategoryModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class DrugManufacturerForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugManufacturerModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class DrugStrengthForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugStrengthModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class DrugUnitForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugUnitModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class DrugForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'category' and field != 'sickness':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = DrugModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
            'category': CheckboxSelectMultiple(attrs={

            }),
            'sickness': CheckboxSelectMultiple(attrs={

            })
        }


class DrugVariantForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'category' and field != 'sickness':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = DrugVariantModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
            'category': CheckboxSelectMultiple(attrs={

            }),
            'sickness': CheckboxSelectMultiple(attrs={

            })
        }


class DrugVariantPriceForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugVariantPriceModel
        fields = '__all__'

        widgets = {

        }


class DrugBatchForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugBatchModel
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Leave Blank to Auto Generate'
            }),

            'date': TextInput(attrs={
                'type': 'date'
            })
        }


class DrugStockForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DrugStockModel
        fields = '__all__'

        widgets = {

        }

