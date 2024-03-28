from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from inventory.models import *
from inventory.forms import *


class InventorySupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = InventorySupplierModel
    permission_required = 'inventory.add_inventorycategorymodel'
    form_class = InventorySupplierForm
    success_message = 'Inventory Supplier Added Successfully'
    template_name = 'inventory/supplier/index.html'

    def get_success_url(self):
        return reverse('inventory_supplier_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_supplier'] = InventorySupplierModel.objects.all().order_by('name')
        return context


class InventorySupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventorySupplierModel
    permission_required = 'inventory.add_inventorycategorymodel'
    fields = '__all__'
    template_name = 'inventory/supplier/index.html'
    context_object_name = "inventory_supplier_list"

    def get_queryset(self):
        return InventorySupplierModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InventorySupplierForm
        return context


class InventorySupplierDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = InventorySupplierModel
    permission_required = 'inventory.add_inventorycategorymodel'
    fields = '__all__'
    template_name = 'inventory/supplier/detail.html'
    context_object_name = "inventory_supplier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_list'] = InventoryStockModel.objects.filter(supplier=self.object)[:20]
        return context


class InventorySupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = InventorySupplierModel
    permission_required = 'inventory.add_inventorycategorymodel'
    form_class = InventorySupplierForm
    success_message = 'Inventory Supplier Updated Successfully'
    template_name = 'inventory/supplier/index.html'

    def get_success_url(self):
        return reverse('inventory_supplier_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_supplier'] = InventorySupplierModel.objects.all().order_by('name')
        return context


class InventorySupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = InventorySupplierModel
    permission_required = 'inventory.add_inventorycategorymodel'
    success_message = 'Inventory Supplier Deleted Successfully'
    fields = '__all__'
    template_name = 'inventory/supplier/delete.html'
    context_object_name = "inventory_supplier"

    def get_success_url(self):
        return reverse('inventory_supplier_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InventoryCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = InventoryCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    form_class = InventoryCategoryForm
    success_message = 'Inventory Category Added Successfully'
    template_name = 'inventory/category/index.html'

    def get_success_url(self):
        return reverse('inventory_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_category_list'] = InventoryCategoryModel.objects.all().order_by('name')
        return context


class InventoryCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventoryCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    fields = '__all__'
    template_name = 'inventory/category/index.html'
    context_object_name = "inventory_category_list"

    def get_queryset(self):
        return InventoryCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InventoryCategoryForm
        return context


class InventoryCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = InventoryCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    form_class = InventoryCategoryForm
    success_message = 'Inventory Category Updated Successfully'
    template_name = 'inventory/category/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_category'] = InventoryCategoryModel.objects.all().order_by('name')
        return context

    def get_success_url(self):
        return reverse('inventory_category_index')


class InventoryCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = InventoryCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    success_message = 'Inventory Category Deleted Successfully'
    fields = '__all__'
    template_name = 'inventory/category/delete.html'
    context_object_name = "inventory_category"

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
            if self.get_object().name.lower() == 'drug':
                messages.error(self.request, 'Cannot Delete Inventory Category Drug')
                return redirect(reverse('inventory_category_index'))
        return super(InventoryCategoryDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('inventory_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InventoryItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = InventoryItemModel
    permission_required = 'inventory.add_inventoryitemmodel'
    form_class = InventoryItemForm
    success_message = 'Inventory Item Added Successfully'
    template_name = 'inventory/item/index.html'

    def get_success_url(self):
        return reverse('inventory_item_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_item_list'] = InventoryItemModel.objects.all().order_by('name')
        context['inventory_category_list'] = InventoryCategoryModel.objects.all().order_by('name')
        return context


class InventoryItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventoryItemModel
    permission_required = 'inventory.view_inventoryitemmodel'
    fields = '__all__'
    template_name = 'inventory/item/index.html'
    context_object_name = "inventory_item_list"

    def get_queryset(self):
        return InventoryItemModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_category_list'] = InventoryCategoryModel.objects.all().order_by('name')

        context['form'] = InventoryItemForm()
        return context


class InventoryItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = InventoryItemModel
    permission_required = 'inventory.view_inventoryitemmodel'
    fields = '__all__'
    template_name = 'inventory/item/detail.html'
    context_object_name = "inventory_item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_category_list'] = InventoryCategoryModel.objects.all().order_by('name')
        context['stock_form'] = InventoryStockForm()
        return context


class InventoryItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = InventoryItemModel
    permission_required = 'inventory.add_inventoryitemmodel'
    form_class = InventoryItemForm
    success_message = 'Inventory Item Updated Successfully'
    template_name = 'inventory/item/index.html'

    def get_success_url(self):
        return reverse('inventory_item_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_item_list'] = InventoryItemModel.objects.all().order_by('name')
        context['inventory_category_list'] = InventoryCategoryModel.objects.all().order_by('name')
        return context


class InventoryItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = InventoryItemModel
    permission_required = 'inventory.add_inventoryitemmodel'
    success_message = 'Inventory Item Deleted Successfully'
    fields = '__all__'
    template_name = 'inventory/item/delete.html'
    context_object_name = "inventory_item"

    def get_success_url(self):
        return reverse('inventory_item_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InventoryStockCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = InventoryStockModel
    permission_required = 'inventory.add_inventoryitemmodel'
    form_class = InventoryStockForm
    success_message = 'Inventory Stocked Successfully'
    template_name = 'inventory/item/detail.html'

    def get_success_url(self):
        return reverse('inventory_item_detail', kwargs={'pk': self.object.item.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_category_list'] = InventoryCategoryModel.objects.all().order_by('name')

        return context


class InventoryStockListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventoryStockModel
    permission_required = 'inventory.view_inventoryitemmodel'
    fields = '__all__'
    template_name = 'inventory/stock/index.html'
    context_object_name = "inventory_stock_list"

    def get_queryset(self):
        return InventoryStockModel.objects.filter().order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class InventoryStockDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = InventoryStockModel
    permission_required = 'inventory.add_inventoryitemmodel'
    success_message = 'Inventory Stock Deleted Successfully'
    fields = '__all__'
    template_name = 'inventory/stock/delete.html'
    context_object_name = "inventory_stock"

    def get_success_url(self):
        return reverse('inventory_item_detail', kwargs={'pk': self.get_object().item.pk})

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.quantity != self.object.quantity_left:
            messages.error(self.request, 'Items in stock given out, stock can no longer be deleted')
            return redirect(reverse('inventory_item_detail', kwargs={'pk': self.object.item.id}))
        if self.request.method == 'POST':
            item = self.object.item
            item.quantity -= self.object.quantity
            item.save()
        return super(InventoryStockDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def stock_out_damaged_inventory(request, pk):
    stock = InventoryStockModel.objects.get(pk=pk)
    if stock.quantity_left <= 0:
        messages.error(request, 'Cannot Stock out of finished Stock')
        return redirect(reverse('inventory_item_detail', kwargs={'pk': stock.item.pk}))

    if request.method == 'POST':
        quantity = float(request.POST.get('quantity'))
        if stock.quantity_left < quantity:
            messages.error(request, 'Stock Out Quantity exceeds stock quantity left')
            return redirect(reverse('inventory_item_detail', kwargs={'pk': stock.item.pk}))

        reason = request.POST.get('reason')
        stock_out = InventoryStockOutModel.objects.create(item=stock.item, quantity=quantity, reason=reason,
                                                          user=request.user)
        stock_out.save()
        if stock_out.id:
            stock.quantity_left -= quantity
            stock.save()

            stock.item.quantity -= quantity
            stock.item.save()

            messages.success(request, '{} units stocked out successfully'.format(quantity))
        else:
            messages.success(request, 'An error occurred, Try Again')
        return redirect(reverse('inventory_item_detail', kwargs={'pk': stock.item.pk}))
    messages.error(request, 'Request Method not Supported')
    return redirect(reverse('inventory_item_detail', kwargs={'pk': stock.item.pk}))


class InventoryStockOutListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventoryStockOutModel
    permission_required = 'inventory.view_inventoryitemmodel'
    fields = '__all__'
    template_name = 'inventory/stock_out/index.html'
    context_object_name = "inventory_stock_out_list"

    def get_queryset(self):
        return InventoryStockOutModel.objects.filter().order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssetCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssetCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    form_class = AssetCategoryForm
    success_message = 'Asset Category Added Successfully'
    template_name = 'inventory/asset_category/index.html'

    def get_success_url(self):
        return reverse('asset_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_category_list'] = AssetCategoryModel.objects.all().order_by('name')
        return context


class AssetCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AssetCategoryModel
    permission_required = 'inventory.view_inventorycategorymodel'
    fields = '__all__'
    template_name = 'inventory/asset_category/index.html'
    context_object_name = "asset_category_list"

    def get_queryset(self):
        return AssetCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AssetCategoryForm
        return context


class AssetCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AssetCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    form_class = AssetCategoryForm
    success_message = 'Asset Category Updated Successfully'
    template_name = 'inventory/asset_category/index.html'

    def get_success_url(self):
        return reverse('asset_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_category_list'] = AssetCategoryModel.objects.all().order_by('name')
        return context


class AssetCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AssetCategoryModel
    permission_required = 'inventory.add_inventorycategorymodel'
    success_message = 'Asset Category Deleted Successfully'
    fields = '__all__'
    template_name = 'inventory/asset_category/delete.html'
    context_object_name = "asset_category"

    def get_success_url(self):
        return reverse('asset_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssetCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssetModel
    permission_required = 'inventory.add_assetmodel'
    form_class = AssetForm
    success_message = 'Asset Added Successfully'
    template_name = 'inventory/asset/index.html'

    def get_success_url(self):
        return reverse('asset_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_list'] = AssetModel.objects.all().order_by('name')
        context['asset_category_list'] = AssetCategoryModel.objects.all().order_by('name')
        return context


class AssetListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AssetModel
    permission_required = 'inventory.view_assetmodel'
    fields = '__all__'
    template_name = 'inventory/asset/index.html'
    context_object_name = "asset_list"

    def get_queryset(self):
        return AssetModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_category_list'] = AssetCategoryModel.objects.all().order_by('name')

        context['form'] = AssetForm()
        return context


class AssetDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AssetModel
    permission_required = 'inventory.view_assetmodel'
    fields = '__all__'
    template_name = 'inventory/asset/detail.html'
    context_object_name = "asset"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_category_list'] = AssetCategoryModel.objects.all().order_by('name')

        return context


class AssetUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AssetModel
    permission_required = 'inventory.add_assetmodel'
    form_class = AssetForm
    success_message = 'Asset Updated Successfully'
    template_name = 'inventory/asset/index.html'

    def get_success_url(self):
        return reverse('asset_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_list'] = AssetModel.objects.all().order_by('name')
        context['asset_category_list'] = AssetCategoryModel.objects.all().order_by('name')
        return context


class AssetDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AssetModel
    permission_required = 'inventory.add_assetmodel'
    success_message = 'Asset Deleted Successfully'
    fields = '__all__'
    template_name = 'inventory/asset/delete.html'
    context_object_name = "asset"

    def get_success_url(self):
        return reverse('asset_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InventoryDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        inventory_list = InventoryItemModel.objects.filter()
        current_inventory_list = InventoryStockModel.objects.filter()
        damage_inventory_list = InventoryStockOutModel.objects.filter()

        total_inventory_worth = 0
        for inventory in inventory_list:
            total_inventory_worth += inventory.quantity * inventory.selling_price

        current_inventory_worth = 0
        for inventory in current_inventory_list:
            current_inventory_worth += inventory.quantity * inventory.unit_cost

        context['total_inventory_worth'] = total_inventory_worth
        context['current_inventory_worth'] = current_inventory_worth

        return context
