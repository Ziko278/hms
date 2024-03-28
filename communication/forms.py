from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput, CheckboxSelectMultiple
from communication.models import *


class NoteForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = NoteModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class ContactCategoryForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ContactCategoryModel
        fields = '__all__'
        widgets = {

        }


class ContactForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ContactModel
        fields = '__all__'
        widgets = {

        }


class SMTPConfigurationForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SMTPConfigurationModel
        fields = '__all__'
        widgets = {
            'password': TextInput(attrs={
                'type': 'password'
            })
        }


class CommunicationSettingForm(ModelForm):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = CommunicationSettingModel
        fields = '__all__'
        widgets = {

        }

