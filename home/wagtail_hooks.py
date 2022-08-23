from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)


from .models import Series


class SeriesAdmin(ModelAdmin):
    model = Series

modeladmin_register(SeriesAdmin)