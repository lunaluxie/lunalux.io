from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from wagtail.signals import page_published

from .models import Article, Series, Contact, InterPageLink, PageHit



class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Contact'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu

    list_display = ('email', 'message', 'name', 'timestamp')
    list_filter = ('email','timestamp')
    search_fields = ('name', 'email', 'message')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(ContactAdmin)


class InterPageLinkAdmin(ModelAdmin):
    model = InterPageLink

modeladmin_register(InterPageLinkAdmin)


# class PageHitAdmin(ModelAdmin):
#     model = PageHit

# modeladmin_register(PageHitAdmin)



def update_interlinks(sender,instance,**kwargs):
    if isinstance(instance, Article):
        instance.add_interpage_links()
page_published.connect(update_interlinks)