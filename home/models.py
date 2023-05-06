from wagtail import blocks
from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from django.shortcuts import redirect
from wagtail.search import index
from .streamfields import body_fields, article_fields, article_header_fields
from bs4 import BeautifulSoup
import datetime
from django.utils import timezone
from collections import Counter

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


    promote_panels = Page.promote_panels + [FieldPanel("image")]
    settings_panels = Page.settings_panels + [FieldPanel("is_project")]

    def get_context(self, request, *args, **kwargs):

        return {}


    class Meta:
        abstract=True

    def type(self):
        return self.__class__.__name__

    def include_image_in_article_list(self):
        if self.is_project:
            return True
        if self.type()=="Series":
            return True
        else:
            return False


    def get_recent_articles(self, n=8):
        return Article.objects.all().filter(live=True).filter(unlisted=False).order_by('-last_published_at')[:n]

    def get_trending_articles(self, n=8):
        queryset = PageHit.objects.all().order_by('-timestamp').filter(page__live=True)
        queryset.filter(timestamp__gte=timezone.now() - datetime.timedelta(days=7))

        queryset = [x.page for x in queryset]
        queryset = [x[0] for x in Counter(queryset).most_common(n)]

        queryset_with_proper_pages = []
        for page in queryset:
            try:
                p = Series.objects.get(pk=page.pk)
                queryset_with_proper_pages.append(p)
            except:
                try:
                    p = Article.objects.get(pk=page.pk)
                    queryset_with_proper_pages.append(p)
                except:
                    pass

        return queryset_with_proper_pages

    def get_all_articles(self):
        return Article.objects.all().filter(live=True).filter(unlisted=False).order_by('-last_published_at')

    def get_recent_projects(self, n=3):
        return Page.objects.all().filter(live=True).filter(is_project=True).order_by('-last_published_at')[:n]


class HomePage(AbstractPage):
    body = StreamField(body_fields, use_json_field=True,null=True, blank=True)

    content_panels = AbstractPage.content_panels + [
        FieldPanel('body'),
    ]

    search_fields = AbstractPage.search_fields + [
        index.SearchField('body'),
    ]


    def get_context(self, request, *args, **kwargs):
        context = super(AbstractPage, self).get_context(request, *args, **kwargs)

        return context


class InterPageLink(models.Model):
    from_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="from_page_related")
    to_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="to_page_related")


class PageHit(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.page.title} - {self.timestamp}"

class Article(AbstractPage):
    header = StreamField(article_header_fields, use_json_field=True, null=True, blank=True)
    body = StreamField(article_fields, use_json_field=True, null=True, blank=True)
    tags = ClusterTaggableManager(through=PageTag, blank=True)

    unlisted = models.BooleanField(default=False)


    content_panels = AbstractPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
        FieldPanel('tags'),
    ]
    settings_panels =AbstractPage.settings_panels + [FieldPanel("unlisted"),]

    search_fields = AbstractPage.search_fields + [
        index.SearchField('body'),
        index.SearchField('tags'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(AbstractPage, self).get_context(request, *args, **kwargs)

        series_id = request.GET.get("series")

        try:
            series = Series.objects.get(id=series_id)
        except:
            series = None

        context["series"] = series

        links = InterPageLink.objects.filter(to_page=self).exclude(from_page=self)
        links = Counter(links).most_common(4)

        context['links'] = links

        return context

    def serve(self, request):

        # create pageview
        PageHit.objects.create(page=self)
        return super().serve(request)


    def add_interpage_links(self):
        soup = BeautifulSoup(str(self.body), 'html.parser')
        links = set()
        for link in soup.findAll("a"):
            links.add(link['href'])

        # print(links)
        for link in links:
            slugList = link.split("/")
            slug = []
            for sl in slugList:
                if sl:
                    slug.append(sl)

            if slug:
                try:
                    p = Article.objects.get(slug=slug[-1])

                    interlink = InterPageLink.objects.get_or_create(from_page=self, to_page=p)

                    # print(p, interlink)

                except:
                    pass

class Series(AbstractPage):
    articles = StreamField([("articles", blocks.ListBlock(blocks.PageChooserBlock()))],
                            use_json_field=True, null=True, blank=True)
    unlisted = models.BooleanField(default=False)

    content_panels = AbstractPage.content_panels + [
                    FieldPanel("articles"),
                    FieldPanel('unlisted'),
            ]

    def serve(self, request):
        # add pageview
        PageHit.objects.create(page=self)

        first_article = self.articles[0].value[0]
        return redirect(f"{first_article.url}?series={self.id}")


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    message = models.TextField()

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
