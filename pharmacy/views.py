from django.shortcuts import render
from pharmacy.models import DrugModel
from django.http import HttpResponse, JsonResponse
from patient.models import PatientModel
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from consultation.models import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from pharmacy.models import *
from pharmacy.forms import *


class DrugCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugCategoryModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugCategoryForm
    success_message = 'Drug Category Added Successfully'
    template_name = 'pharmacy/drug_category/index.html'

    def get_success_url(self):
        return reverse('drug_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_category_list'] = DrugCategoryModel.objects.all().order_by('name')
        return context


class DrugCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugCategoryModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_category/index.html'
    context_object_name = "drug_category_list"

    def get_queryset(self):
        return DrugCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugCategoryForm
        return context


class DrugCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugCategoryModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugCategoryForm
    success_message = 'Drug Category Updated Successfully'
    template_name = 'pharmacy/drug_category/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_category'] = DrugCategoryModel.objects.all().order_by('name')
        return context

    def get_success_url(self):
        return reverse('drug_category_index')


class DrugCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugCategoryModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Category Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_category/delete.html'
    context_object_name = "drug_category"

    def get_success_url(self):
        return reverse('drug_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugManufacturerCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugManufacturerModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugManufacturerForm
    success_message = 'Drug Manufacturer Added Successfully'
    template_name = 'pharmacy/drug_manufacturer/index.html'

    def get_success_url(self):
        return reverse('drug_manufacturer_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_manufacturer_list'] = DrugManufacturerModel.objects.all().order_by('name')
        return context


class DrugManufacturerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugManufacturerModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_manufacturer/index.html'
    context_object_name = "drug_manufacturer_list"

    def get_queryset(self):
        return DrugManufacturerModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugManufacturerForm
        return context


class DrugManufacturerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugManufacturerModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugManufacturerForm
    success_message = 'Drug Manufacturer Updated Successfully'
    template_name = 'pharmacy/drug_manufacturer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_manufacturer'] = DrugManufacturerModel.objects.all().order_by('name')
        return context

    def get_success_url(self):
        return reverse('drug_manufacturer_index')


class DrugManufacturerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugManufacturerModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug manufacturer Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_manufacturer/delete.html'
    context_object_name = "drug_manufacturer"

    def get_success_url(self):
        return reverse('drug_manufacturer_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class DrugStrengthCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugStrengthModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugStrengthForm
    success_message = 'Drug Strength Added Successfully'
    template_name = 'pharmacy/drug_strength/index.html'

    def get_success_url(self):
        return reverse('drug_strength_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_strength_list'] = DrugStrengthModel.objects.all().order_by('name')
        return context


class DrugStrengthListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugStrengthModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_strength/index.html'
    context_object_name = "drug_strength_list"

    def get_queryset(self):
        return DrugStrengthModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugStrengthForm
        return context


class DrugStrengthUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugStrengthModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugStrengthForm
    success_message = 'Drug Strength Updated Successfully'
    template_name = 'pharmacy/drug_strength/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_strength'] = DrugStrengthModel.objects.all().order_by('name')
        return context

    def get_success_url(self):
        return reverse('drug_strength_index')


class DrugStrengthDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugStrengthModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Strength Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_strength/delete.html'
    context_object_name = "drug_strength"

    def get_success_url(self):
        return reverse('drug_strength_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugUnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugUnitModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugUnitForm
    success_message = 'Drug Unit Added Successfully'
    template_name = 'pharmacy/drug_unit/index.html'

    def get_success_url(self):
        return reverse('drug_unit_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_unit_list'] = DrugUnitModel.objects.all().order_by('name')
        return context


class DrugUnitListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugUnitModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_unit/index.html'
    context_object_name = "drug_unit_list"

    def get_queryset(self):
        return DrugUnitModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugUnitForm
        return context


class DrugUnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugUnitModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugUnitForm
    success_message = 'Drug Unit Updated Successfully'
    template_name = 'pharmacy/drug_unit/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_Unit'] = DrugUnitModel.objects.all().order_by('name')
        return context

    def get_success_url(self):
        return reverse('drug_unit_index')


class DrugUnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugUnitModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Unit Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_unit/delete.html'
    context_object_name = "drug_unit"

    def get_success_url(self):
        return reverse('drug_unit_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugForm
    success_message = 'Drug Added Successfully'
    template_name = 'pharmacy/drug/create.html'

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug/index.html'
    context_object_name = "drug_list"

    def get_queryset(self):
        return DrugModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugForm
        return context


class DrugDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DrugModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug/detail.html'
    context_object_name = "drug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manufacturer_list'] = DrugManufacturerModel.objects.all().order_by('name')
        context['strength_list'] = DrugStrengthModel.objects.all().order_by('name')
        context['unit_list'] = DrugUnitModel.objects.all().order_by('name')
        context['form_list'] = DRUG_FORM
        context['variant_form'] = DrugVariantForm
        context['variant_price_form'] = DrugVariantPriceForm
        context['insurance_list'] = INSURANCE_PROVIDER
        return context


class DrugUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugForm
    success_message = 'Drug Updated Successfully'
    template_name = 'pharmacy/drug/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.pk})


class DrugDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug/delete.html'
    context_object_name = "drug"

    def get_success_url(self):
        return reverse('drug_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugVariantCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugVariantModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugVariantForm
    success_message = 'Drug Variant Added Successfully'
    template_name = 'pharmacy/drug/detail.html'

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.drug.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugVariantListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugVariantModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_variant/index.html'
    context_object_name = "drug_variant_list"

    def get_queryset(self):
        return DrugVariantModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugVariantForm
        return context


class DrugVariantUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugVariantModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugVariantForm
    success_message = 'Drug Variant Updated Successfully'
    template_name = 'pharmacy/drug_variant/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.drug.pk})


class DrugVariantDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugVariantModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Variant Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_variant/delete.html'
    context_object_name = "drug_variant"

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.drug.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugVariantPriceCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugVariantPriceModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugVariantPriceForm
    success_message = 'Drug Variant Price Added Successfully'
    template_name = 'pharmacy/drug/detail.html'

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.drug_variant.drug.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugVariantPriceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugVariantPriceModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_variant_price/index.html'
    context_object_name = "drug_variant_price_list"

    def get_queryset(self):
        return DrugVariantPriceModel.objects.all().order_by('drug_variant__drug__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugVariantPriceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugVariantPriceModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugVariantPriceForm
    success_message = 'Drug Variant Price Updated Successfully'
    template_name = 'pharmacy/drug/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.drug_variant.drug.pk})


class DrugVariantPriceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugVariantPriceModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Variant Price Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_variant_price/delete.html'
    context_object_name = "drug_variant_price"

    def get_success_url(self):
        return reverse('drug_detail', kwargs={'pk': self.object.drug_variant.drug.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugBatchCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugBatchModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugBatchForm
    success_message = 'Drug Batch Added Successfully'
    template_name = 'pharmacy/drug_batch/index.html'

    def get_success_url(self):
        return reverse('drug_batch_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_batch_list'] = DrugBatchModel.objects.all().order_by('id').reverse()
        return context


class DrugBatchListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugBatchModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_batch/index.html'
    context_object_name = "drug_batch_list"

    def get_queryset(self):
        return DrugBatchModel.objects.all().order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugBatchForm
        return context


class DrugBatchDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DrugBatchModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_batch/detail.html'
    context_object_name = "drug_batch"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugBatchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugBatchModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugBatchForm
    success_message = 'Drug Batch Updated Successfully'
    template_name = 'pharmacy/drug_batch/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drug_batch'] = DrugBatchModel.objects.all().order_by('name')
        return context

    def get_success_url(self):
        return reverse('drug_batch_index')


class DrugBatchDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugBatchModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Batch Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_batch/delete.html'
    context_object_name = "drug_batch"

    def get_success_url(self):
        return reverse('drug_batch_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugStockCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DrugStockModel
    permission_required = 'academic.add_classesmodel'
    form_class = DrugStockForm
    success_message = 'Drug Stocked Successfully'
    template_name = 'pharmacy/drug_stock/create.html'

    def get_success_url(self):
        return reverse('drug_stock_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = DrugBatchModel.objects.last()

        return context


class DrugStockListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DrugStockModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_stock/index.html'
    context_object_name = "drug_stock_list"

    def get_queryset(self):
        batch_id = self.request.GET.get('batch_id', None)
        if batch_id:
            last_batch = DrugBatchModel.objects.filter(id=batch_id).last()
        else:
            last_batch = DrugBatchModel.objects.last()
        return DrugStockModel.objects.filter(batch=last_batch).order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrugStockForm
        batch_id = self.request.GET.get('batch_id', None)
        if batch_id:
            last_batch = DrugBatchModel.objects.filter(id=batch_id).last()
        else:
            last_batch = DrugBatchModel.objects.last()
        context['last_batch'] = last_batch
        return context


class DrugStockDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DrugStockModel
    permission_required = 'academic.view_classesmodel'
    fields = '__all__'
    template_name = 'pharmacy/drug_stock/detail.html'
    context_object_name = "drug_stock"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DrugStockUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DrugStockModel
    permission_required = 'academic.change_classsesmodel'
    form_class = DrugStockForm
    success_message = 'Drug Stock Updated Successfully'
    template_name = 'pharmacy/drug_stock/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('drug_stock_detail', kwargs={'pk': self.object.pk})


class DrugStockDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DrugStockModel
    permission_required = 'academic.delete_classesmodel'
    success_message = 'Drug Stock Deleted Successfully'
    fields = '__all__'
    template_name = 'pharmacy/drug_stock/delete.html'
    context_object_name = "drug_stock"

    def get_success_url(self):
        return reverse('drug_stock_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def get_drug_from_name(request):
    drug_name = request.GET.get('name', '')
    row = request.GET.get('row', 0)
    list_format = request.GET.get('list_format', '')
    if drug_name:
        drug_list = DrugModel.objects.filter(name__icontains=drug_name).order_by('name')
    else:
        drug_list = None

    if not list_format:
        list_format = 'list'

    context = {
        'drug_list': drug_list,
        'list_format': list_format,
        'row': row
    }
    return render(request, 'pharmacy/partial/drug_list.html', context)


def get_drug_detail_from_id(request):
    drug_id = request.GET.get('id', '')

    if not drug_id:
        return JsonResponse({})

    try:
        drug = DrugModel.objects.get(id=drug_id)
    except ObjectDoesNotExist:
        return JsonResponse({})

    return JsonResponse({
        'id': drug.id,
        'name': drug.name.title(),
        'strength': drug.strength()
    })


def consultation_prescription_create_view(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        patient = PatientModel.objects.get(pk=patient_id)

        drug_list = request.POST.getlist('product_id[]')
        quantity_list = request.POST.getlist('quantity[]')
        dosage_list = request.POST.getlist('dosage_id[]')
        strength_list = request.POST.getlist('strength_id[]')

        last_pres_object = ConsultationPrescriptionModel.objects.last()
        if not last_pres_object:
            pres_id = 1
        else:
            pres_id = last_pres_object.sale_id + 1

        for num in range(len(drug_list)):
            drug = DrugModel.objects.get(pk=drug_list[num])
            quantity = DrugModel.objects.get(pk=quantity_list[num])
            strength = DrugStrengthModel.objects.get(pk=strength_list[num])
            unit = DrugUnitModel.objects.get(pk=dosage_list[num])
            prescription = PrescriptionModel.objects.create(drug=drug, quantity=quantity,
                                                            unit_selling_price=drug.selling_price,
                                                            total_price=drug.selling_price*quantity,
                                                            pres_id=pres_id, strength=strength, unit=unit)
            prescription.save()

        pres_summary = ConsultationPrescriptionModel.objects.create(pres_id=pres_id, patient=patient, )
        pres_summary.save()
        messages.success(request, 'SALE SUCCESSFUL')

        return redirect(reverse('sale_index'))

    return render(request, 'sale/create.html', context=context)