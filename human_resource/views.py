from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
import json
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import io
from xlsxwriter.workbook import Workbook
from django.forms.models import model_to_dict
from human_resource.models import *
from human_resource.forms import *
from django.db.models import Sum
from admin_site.utility import state_list


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DepartmentModel
    permission_required = 'human_resource.add_departmentmodel'
    form_class = DepartmentForm
    template_name = 'human_resource/department/index.html'
    success_message = 'Department Successfully Registered'

    def get_success_url(self):
        return reverse('department_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_list'] = DepartmentModel.objects.all().order_by('name')
        return context


class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DepartmentModel
    permission_required = 'human_resource.add_departmentmodel'
    fields = '__all__'
    template_name = 'human_resource/department/index.html'
    context_object_name = "department_list"

    def get_queryset(self):
        return DepartmentModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepartmentForm
        return context


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DepartmentModel
    permission_required = 'human_resource.add_departmentmodel'
    form_class = DepartmentForm
    template_name = 'human_resource/department/index.html'
    success_message = 'Department Successfully Updated'

    def get_success_url(self):
        return reverse('department_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DepartmentModel
    permission_required = 'human_resource.add_departmentmodel'
    fields = '__all__'
    template_name = 'human_resource/department/delete.html'
    context_object_name = "department"
    success_message = 'Department Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('department_index')


def multi_department_action(request):
    if request.method == 'POST':
        department_list = request.GET.getlist('department')
        department_list = DepartmentModel.objects.filter(id__in=department_list)
        action = request.POST.get('action')
        if action == 'delete':
            for department in department_list:
                department.delete()
            messages.success(request, 'Selected Departments Successfully Deleted')
        else:
            messages.error(request, 'Invalid Request')
        return redirect(reverse('department_index'))
    department_list = request.GET.getlist('department')
    if len(department_list) == 0:
        messages.error(request, 'No Department Selected')
        return redirect(reverse('department_index'))
    action = request.GET.get('action')
    context = {
        'department_list': DepartmentModel.objects.filter(id__in=department_list)
    }
    if action == 'delete':
        return render(request, 'human_resource/department/multi_delete.html', context)
    messages.error(request, 'Invalid Request')
    return redirect(reverse('department_index'))


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = PositionModel
    permission_required = 'human_resource.add_departmentmodel'
    form_class = PositionForm
    template_name = 'human_resource/position/index.html'
    success_message = 'Position Successfully Registered'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['department_list'] = DepartmentModel.objects.all().order_by('name')
        context['position_list'] = PositionModel.objects.all().order_by('name')
        return context


class PositionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PositionModel
    permission_required = 'human_resource.add_departmentmodel'
    fields = '__all__'
    template_name = 'human_resource/position/index.html'
    context_object_name = "position_list"

    def get_queryset(self):
        return PositionModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_list'] = DepartmentModel.objects.all().order_by('name')
        context['form'] = PositionForm

        return context


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PositionModel
    permission_required = 'human_resource.add_departmentmodel'
    form_class = PositionForm
    template_name = 'human_resource/position/index.html'
    success_message = 'Position Successfully Updated'

    def get_success_url(self):
        return reverse('position_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PositionModel
    permission_required = 'human_resource.add_departmentmodel'
    fields = '__all__'
    template_name = 'human_resource/position/delete.html'
    context_object_name = "position"
    success_message = 'Position Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('position_index')


def multi_position_action(request):
    if request.method == 'POST':
        position_list = request.GET.getlist('position')
        position_list = PositionModel.objects.filter(id__in=position_list)
        action = request.POST.get('action')
        if action == 'delete':
            for position in position_list:
                position.delete()
            messages.success(request, 'Selected Positions Successfully Deleted')
        else:
            messages.error(request, 'Invalid Request')
        return redirect(reverse('position_index'))
    position_list = request.GET.getlist('position')
    if len(position_list) == 0:
        messages.error(request, 'No Position Selected')
        return redirect(reverse('position_index'))
    action = request.GET.get('action')
    context = {
        'position_list': PositionModel.objects.filter(id__in=position_list)
    }
    if action == 'delete':
        return render(request, 'human_resource/position/multi_delete.html', context)
    messages.error(request, 'Invalid Request')
    return redirect(reverse('position_index'))


class StaffCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = StaffModel
    permission_required = 'human_resource.add_staffmodel'
    form_class = StaffForm
    template_name = 'human_resource/staff/create.html'
    success_message = 'Staff Successfully Registered'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['department_list'] = DepartmentModel.objects.all().order_by('name')
        context['staff_setting'] = GeneralSettingModel.objects.filter().first()
        context['state_list'] = state_list
        return context


class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StaffModel
    permission_required = 'human_resource.view_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/index.html'
    context_object_name = "staff_list"

    def get_queryset(self):
        return StaffModel.objects.all().order_by(Lower('first_name'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = StaffModel
    permission_required = 'human_resource.view_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/detail.html'
    context_object_name = "staff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['certificate_form'] = StaffCertificateForm
        return context


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StaffModel
    permission_required = 'human_resource.change_staffmodel'
    form_class = StaffEditForm
    template_name = 'human_resource/staff/edit.html'
    success_message = 'Staff Information Successfully Updated'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_list'] = DepartmentModel.objects.all().order_by('name')
        context['staff_setting'] = GeneralSettingModel.objects.filter().first()
        context['state_list'] = state_list
        context['staff'] = self.object
        return context


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StaffModel
    permission_required = 'human_resource.delete_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/delete.html'
    context_object_name = "staff"
    success_message = 'Staff Successfully Deleted'

    def get_success_url(self):
        return reverse('staff_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class StaffCertificateCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = StaffCertificateModel
    permission_required = 'human_resource.change_staffmodel'
    form_class = StaffCertificateForm
    template_name = 'human_resource/staff/detail.html'
    success_message = 'Certificate Successfully Added'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.staff.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StaffCertificateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StaffCertificateModel
    permission_required = 'human_resource.change_staffmodel'
    form_class = StaffCertificateForm
    template_name = 'human_resource/staff/detail.html'
    success_message = 'Certificate Successfully Updated'

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.staff.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StaffCertificateDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StaffCertificateModel
    permission_required = 'human_resource.change_staffmodel'
    fields = '__all__'
    template_name = 'human_resource/staff/cert_delete.html'
    context_object_name = "certificate"
    success_message = 'Certificate Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('staff_detail', kwargs={'pk': self.object.staff.id})


def add_shift_view(request, pk):
    staff = get_object_or_404(StaffModel, pk=pk)
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save()
            staff.shifts.add(shift)
            messages.success(request, 'Shift Added Successfully')
        else:
            messages.warning(request, 'An Error Occurred, Try Later')
    else:
        messages.warning(request, 'Method Not Allowed')
    return redirect(reverse('staff_detail', kwargs={'pk': staff.id}))


def generate_form_view(request):
    if request.method == 'POST':
        staff_list = request.POST.getlist('staff_list[]')
        field_list = request.POST.getlist('form_field[]')
        file_name = request.POST['file_name']
        if not staff_list:
            messages.warning(request, 'No staff Selected')
            return redirect(reverse('staff_form'))
        if not field_list:
            messages.warning(request, 'No Field Selected')
            return redirect(reverse('staff_form'))

        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        for num in range(len(field_list)):
            field = field_list[num]
            worksheet.write(0, num, field.title())

        for row in range(len(staff_list)):
            staff_pk = staff_list[row]
            staff = StaffModel.objects.get(pk=staff_pk)

            for col in range(len(field_list)):
                field = field_list[col]
                if field == 'full_name':
                    value = staff.__str__()
                elif field == 'department':
                    value = staff.department.name.title()
                elif field == 'position':
                    value = staff.position.name.title()
                else:
                    value = getattr(staff, field)
                if isinstance(value, str):
                    value = value.title()
                worksheet.write(row + 1, col, value)
        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename="+file_name+".xlsx"

        output.close()

        return response

    staff_list = StaffModel.objects.filter(status='active').order_by(Lower('first_name'))

    context = {
        'staff_list': staff_list
    }
    return render(request, 'human_resource/staff/generate_form.html', context)
