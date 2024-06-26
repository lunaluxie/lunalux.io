from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.signals import page_published

from home.models.page_models import Article, Series, AbstractPage
from home.models.helper_models import InterPageLink, Contact, PageHit



class ContactAdmin(SnippetViewSet):
    model = Contact
    menu_label = 'Contact'  # ditch this to use verbose_name_plural from model
    menu_name = 'contact'
    icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_admin_menu = True  # or True to add your model to the Settings sub-menu

    list_display = ('email', 'message', 'name', 'timestamp')
    list_filter = ('email','timestamp')
    search_fields = ('name', 'email', 'message')


# Now you just need to register your customised ModelAdmin class with Wagtail
register_snippet(ContactAdmin)


class InterPageLinkAdmin(SnippetViewSet):
    model = InterPageLink

register_snippet(InterPageLinkAdmin)

def update_interlinks(sender,instance,**kwargs):
    if isinstance(instance, AbstractPage):
        instance.add_interpage_links()
page_published.connect(update_interlinks)