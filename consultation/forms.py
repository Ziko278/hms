from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput
from consultation.models import *


class ConsultationBlockForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ConsultationBlockModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class ConsultationRoomForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ConsultationRoomModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class ConsultationFeeForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ConsultationFeeModel
        fields = '__all__'
        widgets = {

        }


class ConsultationForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ConsultationModel
        fields = '__all__'
        widgets = {

        }
        