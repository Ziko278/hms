from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Select, TextInput, Textarea, CheckboxSelectMultiple, DateInput
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from admin_site.models import *


class SiteInfoForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SiteInfoModel
        fields = '__all__'
        exclude = ["title", "author", "keywords", "description"]
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:50px'
            })
        }


class GeneralSettingForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in []:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = GeneralSettingModel
        fields = '__all__'
        widgets = {

        }
