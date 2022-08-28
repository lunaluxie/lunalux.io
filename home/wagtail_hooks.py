from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)


from .models import Series, Contact


class SeriesAdmin(ModelAdmin):
    model = Series

modeladmin_register(SeriesAdmin)


class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Contact'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    # or True to exclude pages of this type from Wagtail's explorer view
    exclude_from_explorer = False
    list_display = ('name', 'email', 'message')
    list_filter = ('name',)
    search_fields = ('name', 'email', 'message')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ContactAdmin)
