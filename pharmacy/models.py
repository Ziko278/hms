from django.db import models
from admin_site.model_info import INSURANCE_PROVIDER, DRUG_FORM
from medication.models import SicknessModel
from django.contrib.auth.models import User
from datetime import date


class DrugCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class DrugManufacturerModel(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name.upper()


class DrugStrengthModel(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name.upper()


class DrugUnitModel(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name.upper()


class DrugModel(models.Model):
    name = models.CharField(max_length=250)
    category = models.ManyToManyField(DrugCategoryModel, blank=True)
    sickness = models.ManyToManyField(SicknessModel, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name.upper()

    def strength(self):
        availability_list = DrugVariantModel.objects.filter(drug=self)
        avail_list = []
        for avail in availability_list:
            avail_list.append(avail.strength.name.lower())
        return avail_list


class DrugVariantModel(models.Model):
    drug = models.ForeignKey(DrugModel, on_delete=models.CASCADE, related_name='drug_variants')
    manufacturer = models.ForeignKey(DrugManufacturerModel, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(DrugUnitModel, on_delete=models.SET_NULL, null=True, blank=True)
    strength = models.ForeignKey(DrugStrengthModel, on_delete=models.SET_NULL, null=True, blank=True)
    form = models.CharField(max_length=50, choices=DRUG_FORM, default='capsule', blank=True, null=True)
    quantity = models.FloatField(blank=True, default=0)
    low_limit = models.IntegerField(default=0)

    def __str__(self):
        drug_name = ''
        drug_name += self.manufacturer.__str__() + ' ' if self.manufacturer else ''
        drug_name += self.strength.__str__() + ' ' if self.strength else ''
        drug_name += self.drug.__str__()
        drug_name += " ({})".format(self.unit.__str__()) if self.unit else ''
        drug_name += " ({})".format(self.form.upper()) if self.form else ''
        return drug_name


class DrugVariantPriceModel(models.Model):
    """"""
    drug_variant = models.ForeignKey(DrugVariantModel, on_delete=models.CASCADE, related_name='variant_prices')
    insurance = models.CharField(max_length=100, blank=True, null=True, choices=INSURANCE_PROVIDER)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{} - N{}".format(self.drug_variant.__str__(), self.amount)


class DrugBatchModel(models.Model):
    name = models.CharField(max_length=250, blank=True)
    date = models.DateField(blank=True)

    def __str__(self):
        return self.name.upper()

    def save(self, *args, **kwargs):
        if not self.name:
            last_batch = DrugBatchModel.objects.last()
            if last_batch:
                last_id = last_batch.id + 1
            else:
                last_id = 1
            while True:
                batch_name = 'batch-' + str(last_id).rjust(4, '0')
                batch_exist = DrugBatchModel.objects.filter(name=batch_name).first()
                if not batch_exist:
                    break
                else:
                    last_id += 1
            self.name = batch_name
        if not self.date:
            self.date = date.today()

        super(DrugBatchModel, self).save(*args, **kwargs)


class DrugStockModel(models.Model):
    drug_variant = models.ForeignKey(DrugVariantModel, on_delete=models.CASCADE)
    batch = models.ForeignKey(DrugBatchModel, on_delete=models.CASCADE, blank=True, null=True)
    quantity_bought = models.FloatField()
    quantity_left = models.FloatField(blank=True, default=0)
    total_cost_price = models.FloatField(blank=True, null=True)
    unit_cost_price = models.FloatField()
    selling_price = models.FloatField()
    current_worth = models.FloatField(default=0, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, default='active')
    date = models.DateField(auto_now_add=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.drug_variant.__str__())

    def save(self, *args, **kwargs):
        if not self.id:
            self.drug_variant.quantity += self.quantity_bought
            self.drug_variant.save()
        if not self.total_cost_price:
            self.total_cost_price = self.unit_cost_price * self.quantity_bought
        if not self.batch:
            last_batch = DrugBatchModel.objects.last()
            self.batch = last_batch if last_batch else None

        if not self.date:
            self.date = date.today()

        if not self.quantity_left:
            self.quantity_left = self.quantity_bought

        self.current_worth = self.quantity_left * self.selling_price

        super(DrugStockModel, self).save(*args, **kwargs)


class DrugStockOutModel(models.Model):
    """"""
    stock = models.ForeignKey(DrugStockModel, on_delete=models.CASCADE)
    drug = models.ForeignKey(DrugModel, on_delete=models.CASCADE)
    quantity = models.FloatField()
    worth = models.FloatField()
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.stock.drug_variant.name

