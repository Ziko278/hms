from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput
from human_resource.models import *


class DepartmentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DepartmentModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class PositionForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = DepartmentModel.objects.all().order_by('name')
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = PositionModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class StaffForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all().order_by('name')

        for field in self.fields:
            if field != 'is_doctor':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StaffModel
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'employment_date': DateInput(attrs={
                'type': 'date'
            }),
            'is_doctor': CheckboxInput(attrs={

            }),
            'medical_conditions': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class StaffEditForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all().order_by('name')
        for field in self.fields:
            if field != 'is_doctor':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = StaffModel
        exclude = []
        widgets = {
            'date_of_birth': DateInput(attrs={
                'type': 'date'
            }),
            'employment_date': DateInput(attrs={
                'type': 'date'
            }),
            'staff_id': TextInput(attrs={
                'readonly': True
            }),
            'medical_conditions': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class StaffCertificateForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = StaffCertificateModel
        fields = '__all__'
        widgets = {
            'date_obtained': DateInput(attrs={
                'type': 'date'
            }),
        }


class ShiftForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = ShiftModel
        fields = '__all__'
        widgets = {
            'date_obtained': DateInput(attrs={
                'type': 'date'
            }),
        }

