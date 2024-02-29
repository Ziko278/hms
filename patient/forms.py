from django.forms import ModelForm, Select, TextInput, DateInput
from patient.models import PatientModel, PatientVitalsModel


class PatientForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = PatientModel
        fields = '__all__'
        exclude = ['number_of_visits', 'last_visit']
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),

            'medical_conditions': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class PatientEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = PatientModel
        fields = '__all__'
        exclude = ['registration_payment', 'user']
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'medical_conditions': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class PatientVitalsForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = PatientVitalsModel
        fields = '__all__'
        exclude = []
        widgets = {

        }
