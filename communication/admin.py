from django.contrib import admin
from communication.models import RecentActivityModel, NoteModel


admin.site.register(RecentActivityModel)
admin.site.register(NoteModel)
