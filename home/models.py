from argparse import _MutuallyExclusiveGroup
from tkinter import N
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from sortedm2m.fields import SortedManyToManyField

from .streamfields import body_fields, article_fields, article_header_fields

class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        'Article',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class AbstractPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    is_project = models.BooleanField(default=False)


    promote_panels = Page.promote_panels + [ImageChooserPanel("image")]
    settings_panels = Page.settings_panels + [FieldPanel("is_project")]

    def get_context(self, request, *args, **kwargs):

        return {}


    class Meta:
        abstract=True


    def get_recent_articles(self, n=8):
        return Article.objects.all().filter(live=True).order_by('-last_published_at')[:n]

    def get_all_articles(self):
        return Article.objects.all().filter(live=True).order_by('-last_published_at')

    def get_recent_projects(self, n=3):
        return Page.objects.all().filter(live=True).filter(is_project=True).order_by('-last_published_at')[:n]


class HomePage(AbstractPage):
    body = StreamField(body_fields, use_json_field=True,null=True, blank=True)

    content_panels = AbstractPage.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(AbstractPage, self).get_context(request, *args, **kwargs)



        return context


class Article(AbstractPage):
    header = StreamField(article_header_fields, null=True, blank=True)
    body = StreamField(article_fields, use_json_field=True,null=True, blank=True)
    tags = ClusterTaggableManager(through=PageTag, blank=True)

    unlisted = models.BooleanField(default=False)


    content_panels = AbstractPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
        FieldPanel('tags'),
    ]


    settings_panels =AbstractPage.settings_panels + [FieldPanel("unlisted"),]

    def get_context(self, request, *args, **kwargs):
        context = super(AbstractPage, self).get_context(request, *args, **kwargs)

        print(Article.objects.all())

        return context

class Series(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)


    articles = SortedManyToManyField(Article)

    unlisted = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    panels = [FieldPanel("name"),
              FieldPanel("description"),
              FieldPanel("articles"),
              FieldPanel('unlisted'),]

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    message = models.TextField()

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
