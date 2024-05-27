from wagtail import blocks
from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
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
from wagtail.search import index
from django.db.models import Count, F, Q
from django.db.models import Case, When

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
        # Get the queryset of PageHit objects
        queryset = PageHit.objects.all()

        # Filter the queryset to include only the PageHits from the last 7 days
        queryset = queryset.filter(timestamp__gte=timezone.now() - datetime.timedelta(days=7))

        # Count the number of occurrences of each page
        page_counts = queryset.values('page').annotate(count=Count('page'))

        # Get the top n pages with the highest count
        top_pages = page_counts.order_by('-count')

        # preserve order of top_pages
        # https://gist.github.com/balazs-endresz/fd4efda41d4581631f4c
        ordering = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(top_pages.values_list('page', flat=True))])

        # Get the queryset of Article and Series objects with the proper pages
        queryset_with_proper_pages = Article.objects.filter(
            Q(pk__in=top_pages.values('page')),
            ~Q(unlisted=True)
        ).order_by(ordering)[:n]

        if not queryset_with_proper_pages:
            return self.get_recent_articles(n=n)

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
        index.FilterField('unlisted')
    ]

    def get_template(self, request, *args, **kwargs):
        if request.META.get('HTTP_HX_REQUEST'):
            return "home/article_partial.html"

        return "home/article.html"

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

        context["HTMX"] = request.META.get('HTTP_HX_REQUEST')

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
