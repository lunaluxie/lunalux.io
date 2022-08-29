from wagtail.core import blocks
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from django.shortcuts import redirect
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

        series_id = request.GET.get("series")

        try:
            series = Series.objects.get(id=series_id)
        except:
            series = None

        articles = series.articles
        for article in articles:
            print (article)
        # print(context)
        # print(series)
        # print(articles)


        context["series"] = series
        # context["series_articles"] = articles

        return context

class Series(AbstractPage):
    articles = StreamField([("articles", blocks.ListBlock(blocks.PageChooserBlock()))],
                            use_json_field=True, null=True, blank=True)
    unlisted = models.BooleanField(default=False)

    content_panels = AbstractPage.content_panels + [FieldPanel("articles"),
                      FieldPanel('unlisted'),]

    def serve(self, request):
        first_article = self.articles[0].value[0]
        return redirect(f"{first_article.url}?series={self.id}")


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    message = models.TextField()

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
