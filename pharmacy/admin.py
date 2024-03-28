from django.contrib import admin
from pharmacy.models import *


admin.site.register(DrugModel)
admin.site.register(DrugUnitModel)
admin.site.register(DrugCategoryModel)
admin.site.register(DrugStrengthModel)
admin.site.register(DrugBatchModel)
admin.site.register(DrugStockModel)
admin.site.register(DrugVariantModel)

