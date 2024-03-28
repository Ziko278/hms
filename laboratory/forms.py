from django.forms import ModelForm, Select, TextInput, DateInput, CheckboxInput, CheckboxSelectMultiple
from laboratory.models import *
from medication.models import SicknessModel


class TestUnitForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TestUnitModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class TestObservationForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TestObservationModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class TestFieldForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TestFieldModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }


class TestForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['fields'].queryset = TestFieldModel.objects.all().order_by('name')
            self.fields['possible_sicknesses'].queryset = SicknessModel.objects.all().order_by()
            if field != 'fields' and field != 'possible_sicknesses':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })

    class Meta:
        model = TestModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:50px'
            }),
            'fields': CheckboxSelectMultiple(attrs={

            }),
            'possible_sicknesses': CheckboxSelectMultiple(attrs={

            })
        }


class TestPriceForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = TestPriceModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:100px'
            }),
        }

