from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, TextInput, RadioSelect, CheckboxInput, CheckboxSelectMultiple, DateInput
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from inventory.models import *


class InventorySupplierForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = InventorySupplierModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
            'address': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class InventoryCategoryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = InventoryCategoryModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class InventoryItemForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = InventoryCategoryModel.objects.filter().order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = InventoryItemModel
        fields = '__all__'

        widgets = {

        }


class InventoryStockForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = InventoryStockModel
        fields = '__all__'

        widgets = {
            'date': DateInput(attrs={
                'type': 'date'
            })
        }


class InventoryStockOutForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = InventoryStockOutModel
        fields = '__all__'

        widgets = {
            'date': DateInput(attrs={
                'type': 'date'
            })
        }


class AssetCategoryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = AssetCategoryModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class AssetForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = AssetModel
        fields = '__all__'

        widgets = {
            'description': TextInput(attrs={
                'style': 'height:60px'
            }),
        }


