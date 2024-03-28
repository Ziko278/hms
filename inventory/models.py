from django.db import models
from django.contrib.auth.models import User
from datetime import date
from admin_site.model_info import *


class InventorySupplierModel(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()
    contact_name = models.CharField(max_length=250, null=True, blank=True)
    contact_phone_number = models.CharField(max_length=100, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=ACTIVE_STATUS, default=ACTIVE_STATUS[0])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class InventoryCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class InventoryItemModel(models.Model):
    category = models.ForeignKey(InventoryCategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    quantity = models.FloatField(null=True, blank=True, default=0)
    selling_price = models.FloatField(null=True, blank=True, default=0)
    low_limit = models.IntegerField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class InventoryStockModel(models.Model):
    item = models.ForeignKey(InventoryItemModel, on_delete=models.CASCADE, related_name='stock_list')
    supplier = models.ForeignKey(InventorySupplierModel, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField()
    quantity_left = models.FloatField(blank=True)
    unit_cost = models.FloatField()
    unit_selling = models.FloatField()
    total_cost_price = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True)
    current_worth = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.item.selling_price = self.unit_selling
        if not self.id:
            self.item.quantity += self.quantity
        self.item.save()
        if not self.quantity_left:
            self.quantity_left = self.quantity
        if not self.total_cost_price:
            self.total_cost_price = self.unit_cost * self.quantity
        if not self.date:
            self.date = date.today()

        self.current_worth = self.quantity_left * self.unit_selling
        super(InventoryStockModel, self).save(*args, **kwargs)


class InventoryStockOutModel(models.Model):
    item = models.ForeignKey(InventoryItemModel, on_delete=models.CASCADE)
    quantity = models.FloatField()
    worth = models.FloatField(blank=True, null=True, default=0)
    reason = models.TextField(null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.worth:
            self.worth = self.quantity * self.item.selling_price
        super(InventoryStockOutModel, self).save(*args, **kwargs)


class AssetCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class AssetModel(models.Model):
    category = models.ForeignKey(AssetCategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    quantity = models.FloatField()
    worth = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()
