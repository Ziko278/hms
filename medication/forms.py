from django.forms import ModelForm, Select, TextInput, DateInput
from django.utils import timezone

from medication.models import BedModel, WardModel, AdmissionModel, AdmissionPaymentModel, DeliveryModel, \
    SicknessModel, DeliveryBabyModel, DeliveryPaymentModel


class SicknessForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = SicknessModel
        fields = '__all__'
        widgets = {
            'description': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class WardForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = WardModel
        fields = '__all__'
        widgets = {

        }


class BedForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = BedModel
        fields = '__all__'
        widgets = {

        }


class AdmissionForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = AdmissionModel
        fields = '__all__'
        widgets = {
            'purpose': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class DeliveryForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DeliveryModel
        fields = '__all__'
        widgets = {
            'purpose': TextInput(attrs={
                'style': 'height:50px'
            }),
        }


class AdmissionDischargeForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['discharge_date'] = timezone.now().date()
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = AdmissionModel
        fields = ['discharge_user', 'discharge_note', 'discharge_date', 'patient_discharge_status', 'status']
        widgets = {
            'discharge_note': TextInput(attrs={
                'style': 'height:100px'
            }),
            'discharge_date': TextInput(attrs={
                'type': 'date'
            }),
        }


class DeliveryDischargeForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['discharge_date'] = timezone.now().date()
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DeliveryModel
        fields = ['discharge_user', 'discharge_note', 'discharge_date', 'patient_status', 'status']
        widgets = {
            'discharge_note': TextInput(attrs={
                'style': 'height:100px'
            }),
            'discharge_date': TextInput(attrs={
                'type': 'date'
            }),
        }


class DeliveryBabyForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['discharge_date'] = timezone.now().date()
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DeliveryBabyModel
        fields = '__all__'
        widgets = {
            'delivery_date': TextInput(attrs={
                'type': 'date'
            }),
            'delivery_time': TextInput(attrs={
                'type': 'time'
            })
        }


class AdmissionPaymentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = AdmissionPaymentModel
        fields = '__all__'
        widgets = {

        }


class DeliveryPaymentForm(ModelForm):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = DeliveryPaymentModel
        fields = '__all__'
        widgets = {

        }
