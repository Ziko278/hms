from django.urls import path
from pharmacy.views import *


urlpatterns = [
    path('drug-category/create', DrugCategoryCreateView.as_view(), name='drug_category_create'),
    path('drug-category/index', DrugCategoryListView.as_view(), name='drug_category_index'),
    path('drug-category/<int:pk>/edit', DrugCategoryUpdateView.as_view(), name='drug_category_edit'),
    path('drug-category/<int:pk>/delete', DrugCategoryDeleteView.as_view(), name='drug_category_delete'),

    path('drug-manufacturer/create', DrugManufacturerCreateView.as_view(), name='drug_manufacturer_create'),
    path('drug-manufacturer/index', DrugManufacturerListView.as_view(), name='drug_manufacturer_index'),
    path('drug-manufacturer/<int:pk>/edit', DrugManufacturerUpdateView.as_view(), name='drug_manufacturer_edit'),
    path('drug-manufacturer/<int:pk>/delete', DrugManufacturerDeleteView.as_view(), name='drug_manufacturer_delete'),

    path('drug-strength/create', DrugStrengthCreateView.as_view(), name='drug_strength_create'),
    path('drug-strength/index', DrugStrengthListView.as_view(), name='drug_strength_index'),
    path('drug-strength/<int:pk>/edit', DrugStrengthUpdateView.as_view(), name='drug_strength_edit'),
    path('drug-strength/<int:pk>/delete', DrugStrengthDeleteView.as_view(), name='drug_strength_delete'),

    path('drug-unit/create', DrugUnitCreateView.as_view(), name='drug_unit_create'),
    path('drug-unit/index', DrugUnitListView.as_view(), name='drug_unit_index'),
    path('drug-unit/<int:pk>/edit', DrugUnitUpdateView.as_view(), name='drug_unit_edit'),
    path('drug-unit/<int:pk>/delete', DrugUnitDeleteView.as_view(), name='drug_unit_delete'),

    path('drug/create', DrugCreateView.as_view(), name='drug_create'),
    path('drug/index', DrugListView.as_view(), name='drug_index'),
    path('drug/<int:pk>/detail', DrugDetailView.as_view(), name='drug_detail'),
    path('drug/<int:pk>/edit', DrugUpdateView.as_view(), name='drug_edit'),
    path('drug/<int:pk>/delete', DrugDeleteView.as_view(), name='drug_delete'),

    path('drug-variant/create', DrugVariantCreateView.as_view(), name='drug_variant_create'),
    path('drug-variant/index', DrugVariantListView.as_view(), name='drug_variant_index'),
    path('drug-variant/<int:pk>/edit', DrugVariantUpdateView.as_view(), name='drug_variant_edit'),
    path('drug-variant/<int:pk>/delete', DrugVariantDeleteView.as_view(), name='drug_variant_delete'),

    path('drug-variant-price/create', DrugVariantPriceCreateView.as_view(), name='drug_variant_price_create'),
    path('drug-variant-price/index', DrugVariantPriceListView.as_view(), name='drug_variant_price_index'),
    path('drug-variant-price/<int:pk>/edit', DrugVariantPriceUpdateView.as_view(), name='drug_variant_price_edit'),
    path('drug-variant-price/<int:pk>/delete', DrugVariantPriceDeleteView.as_view(), name='drug_variant_price_delete'),

    path('drug-batch/create', DrugBatchCreateView.as_view(), name='drug_batch_create'),
    path('drug-batch/index', DrugBatchListView.as_view(), name='drug_batch_index'),
    path('drug-batch/<int:pk>/detail', DrugBatchDetailView.as_view(), name='drug_batch_detail'),
    path('drug-batch/<int:pk>/edit', DrugBatchUpdateView.as_view(), name='drug_batch_edit'),
    path('drug-batch/<int:pk>/delete', DrugBatchDeleteView.as_view(), name='drug_batch_delete'),

    path('drug-stock/create', DrugStockCreateView.as_view(), name='drug_stock_create'),
    path('drug-stock/index', DrugStockListView.as_view(), name='drug_stock_index'),
    path('drug-stock/<int:pk>/detail', DrugStockDetailView.as_view(), name='drug_stock_detail'),
    path('drug-stock/<int:pk>/edit', DrugStockUpdateView.as_view(), name='drug_stock_edit'),
    path('drug-stock/<int:pk>/delete', DrugStockDeleteView.as_view(), name='drug_stock_delete'),

    path('get-drug-from-name', get_drug_from_name, name='get_drug_from_name'),
    path('get-drug-detail-from-id', get_drug_detail_from_id, name='get_drug_detail_from_id'),

]



