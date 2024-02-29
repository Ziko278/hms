from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from laboratory.models import *
from laboratory.forms import *


class TestUnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TestUnitModel
    permission_required = 'laboratory.add_testunitmodel'
    form_class = TestUnitForm
    template_name = 'laboratory/test_unit/index.html'
    success_message = 'Test Unit Successfully Added'

    def get_success_url(self):
        return reverse('test_unit_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_unit_list'] = TestUnitModel.objects.all().order_by('name')
        return context


class TestUnitListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TestUnitModel
    permission_required = 'laboratory.view_testunitmodel'
    fields = '__all__'
    template_name = 'laboratory/test_unit/index.html'
    context_object_name = "test_unit_list"

    def get_queryset(self):
        return TestUnitModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TestUnitForm
        return context


class TestUnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TestUnitModel
    permission_required = 'laboratory.change_testunitmodel'
    form_class = TestUnitForm
    template_name = 'laboratory/test_unit/index.html'
    success_message = 'Test Unit Successfully Updated'

    def get_success_url(self):
        return reverse('test_unit_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestUnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TestUnitModel
    permission_required = 'laboratory.delete_testunitmodel'
    fields = '__all__'
    template_name = 'laboratory/test_unit/delete.html'
    context_object_name = "test_unit"
    success_message = 'Test Unit Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('test_unit_index')


class TestFieldCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TestFieldModel
    permission_required = 'laboratory.add_testfieldmodel'
    form_class = TestFieldForm
    template_name = 'laboratory/test_field/index.html'
    success_message = 'Test Field Successfully Added'

    def get_success_url(self):
        return reverse('test_field_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['test_unit_list'] = TestUnitModel.objects.all().order_by('name')
        context['test_field_list'] = TestFieldModel.objects.all().order_by('name')
        return context


class TestFieldListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TestFieldModel
    permission_required = 'laboratory.view_testfieldmodel'
    fields = '__all__'
    template_name = 'laboratory/test_field/index.html'
    context_object_name = "test_field_list"

    def get_queryset(self):
        return TestFieldModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_unit_list'] = TestUnitModel.objects.all().order_by('name')
        context['form'] = TestFieldForm

        return context


class TestFieldUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TestFieldModel
    permission_required = 'laboratory.change_testfieldmodel'
    form_class = TestFieldForm
    template_name = 'laboratory/test_field/index.html'
    success_message = 'Test Field Successfully Updated'

    def get_success_url(self):
        return reverse('test_field_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestFieldDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TestFieldModel
    permission_required = 'laboratory.delete_test_fieldmodel'
    fields = '__all__'
    template_name = 'laboratory/test_field/delete.html'
    context_object_name = "test_field"
    success_message = 'Test Field Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('test_field_index')


class TestCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TestModel
    permission_required = 'laboratory.add_testmodel'
    form_class = TestForm
    template_name = 'laboratory/test/create.html'
    success_message = 'Laboratory Test Successfully Added'

    def get_success_url(self):
        return reverse('test_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TestFieldModel
    permission_required = 'laboratory.view_testmodel'
    fields = '__all__'
    template_name = 'laboratory/test/index.html'
    context_object_name = "test_list"

    def get_queryset(self):
        return TestModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = TestModel
    permission_required = 'laboratory.view_testmodel'
    fields = '__all__'
    template_name = 'laboratory/test/detail.html'
    context_object_name = "test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_form'] = TestPriceForm
        context['insurance_list'] = INSURANCE_PROVIDER
        return context


class TestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TestModel
    permission_required = 'laboratory.change_testmodel'
    form_class = TestForm
    template_name = 'laboratory/test/edit.html'
    success_message = 'Laboratory Test Successfully Updated'

    def get_success_url(self):
        return reverse('test_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TestModel
    permission_required = 'laboratory.delete_testmodel'
    fields = '__all__'
    template_name = 'laboratory/test/delete.html'
    context_object_name = "test"
    success_message = 'Laboratory Test Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('test_index')


class TestPriceCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TestPriceModel
    permission_required = 'laboratory.add_testpricemodel'
    form_class = TestPriceForm
    template_name = 'laboratory/test/detail.html'
    success_message = 'Laboratory Test Price Successfully Added'

    def get_success_url(self):
        return reverse('test_detail', kwargs={'pk': self.object.test.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestPriceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TestPriceModel
    permission_required = 'laboratory.change_testpricemodel'
    form_class = TestPriceForm
    template_name = 'laboratory/test/detail.html'
    success_message = 'Laboratory Test Successfully Updated'

    def get_success_url(self):
        return reverse('test_detail', kwargs={'pk': self.object.test.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TestPriceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TestPriceModel
    permission_required = 'laboratory.delete_testpricemodel'
    fields = '__all__'
    template_name = 'laboratory/test/price_delete.html'
    context_object_name = "test_price"
    success_message = 'Laboratory Test Price Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('test_detail', kwargs={'pk': self.object.test.pk})


class ConsultationTestListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConductTestModel
    permission_required = 'consultation.view_conducttestmodel'
    fields = '__all__'
    template_name = 'laboratory/lab_test/index.html'
    context_object_name = "lab_test_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return ConductTestModel.objects.filter(date__gte=start_date, date__lte=end_date, payment_made=True).order_by('date').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        if not start_date:
            start_date = end_date = date.today()
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        context['start_date'] = start_date
        context['end_date'] = end_date

        return context


class ConsultationTestDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ConductTestModel
    permission_required = 'consultation.view_conducttestmodel'
    fields = '__all__'
    template_name = 'laboratory/lab_test/detail.html'
    context_object_name = "lab_test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def test_sample_collection_view(request, pk):
    if request.method == 'POST':
        test = get_object_or_404(ConductTestModel, pk=pk)
        sample_label = request.POST.get('sample_label', '')
        sample_collected = True if 'sample_collected' in request.POST else False
        test.sample_label = sample_label
        test.sample_collected = sample_collected
        test.save()

        messages.success(request, 'Test Sample Record Updated Successfully')
        previous_url = request.META.get('HTTP_REFERER', reverse('lab_test_index'))

        return redirect(previous_url)

    raise PermissionError('Method Not Supported, Permission Denied')


def test_result_record_view(request, pk):
    test = get_object_or_404(ConductTestModel, pk=pk)
    test_result = ConductTestResultModel.objects.filter(test=test).first()

    if request.method == 'POST':
        test_field_list = test.test.fields.all()
        comment = request.POST.get('lab_attendant_comment', '')

        result_record = {}
        for field in test_field_list:
            if '{}'.format(field.name.lower()) in request.POST:
                field_result = request.POST.get('{}'.format(field.name.lower())).strip()
                try:
                    field_result = float(field_result)
                except ValueError:
                    pass
                result_record[field.name.lower()] = {
                    'value': field_result,
                    'normal_range': field.range(),
                    'low_limit': field.normal_lower_limit,
                    'high_limit': field.normal_upper_limit,

                }
        if 'result_ready' in request.POST:
            test.result_ready = True
        else:
            test.result_ready = False
        test.save()

        if test_result:
            test_result.test_result = result_record
        else:
            test_result = ConductTestResultModel.objects.create(test=test, test_result=result_record,
                                            attendant=request.user)
        test_result.lab_attendant_comment=comment
        test_result.save()

        if test_result.id:
            messages.success(request, 'Test Results Recorded successfully')

        return redirect(reverse('lab_test_detail', kwargs={'pk': test.pk}))

    context = {
        'lab_test': test,
        'test_result': test_result
    }
    return render(request, 'laboratory/lab_test/record_result.html', context)
