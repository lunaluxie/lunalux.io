import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.models import Tag
from wagtail import hooks
from wagtail.admin.panels import FieldPanel
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
from wagtail.search import index
from wagtail.search.signal_handlers import register_signal_handlers
from wagtail.signals import page_published
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from home.models.helper_models import Contact, InterPageLink, PageHit
from home.models.page_models import AbstractPage, Article, Series


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
    list_display = ("id", "from_page__url", "to_page__url")
    search_fields = ("from_page__url", "to_page__url")
    list_filter = ('from_page','to_page')
    icon = "link"
    model = InterPageLink

register_snippet(InterPageLinkAdmin)

def update_interlinks(sender,instance,**kwargs):
    if isinstance(instance, AbstractPage):
        instance.add_interpage_links()
page_published.connect(update_interlinks)


class TagsSnippetViewSet(SnippetViewSet):
    panels = [FieldPanel("name")]  # only show the name field
    model = Tag
    icon = "tag"  # change as required
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 400
    list_display = ["name", "slug"]
    search_fields = ("name",)

register_snippet(TagsSnippetViewSet)


@hooks.register('register_rich_text_features')
def register_strong_feature(features):
    """
    Registering the `muted` feature. It will render bold text with `muted` tag.
    """
    feature_name = 'muted'
    type_ = 'MUTED'
    tag = 'muted'

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'icon': 'radio-empty',
        'description': 'Text will appear muted.',
        'style': {'color': '#666'},
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)


register_signal_handlers()