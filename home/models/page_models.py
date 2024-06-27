from wagtail import blocks
from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from django.shortcuts import redirect
from wagtail.search import index
from home.streamfields import body_fields, article_fields, article_header_fields
from bs4 import BeautifulSoup
import datetime
from django.utils import timezone
from collections import Counter
from wagtail.search import index
from django.db.models import Count, F, Q
from django.db.models import Case, When

from home.models.helper_models import PageTag, InterPageLink, PageHit, Contact


class AbstractPage(Page):
    page_description = "The base page which all all other subpages inherit from. This page should not be used directly. Does not contain any content."

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    is_project = models.BooleanField(default=False, help_text="Will show up in projects section")
    unlisted = models.BooleanField(default=False, help_text="If unlisted, the article will be publically accessible, and indexable by search engine, but will not show up in search, or in the list of articles on the homepage")


    garden_status = [
        ("na", "None"),
        ("seedling", "🌱 Seedling: For rough and early ideas"),
        ("budding", "🌿 Budding: For work that has been cleaned up and clarified"),
        ("evergreen", "🌳 Evergreen: For work that's reasonably complete, but might still receive updates."),
    ]
    garden_status = models.CharField(choices=garden_status, max_length=10, default="na", help_text="If set, the page will show up in the garden section of the site.")

    tags = ClusterTaggableManager(through=PageTag, blank=True)

    promote_panels = [MultiFieldPanel([
                         FieldPanel("image", heading="Search Image", help_text="Image to show up in search results (including for promotion on site)"),
                         FieldPanel("slug"),
                         FieldPanel("seo_title"),
                         FieldPanel("search_description"),
                        ],
                        heading="For Search Engines",
                        help_text="Settings that affect how the page will show up in search engines."
                    ),
                     MultiFieldPanel([
                                     FieldPanel("is_project"),
                                     FieldPanel("garden_status"),
                                     FieldPanel("unlisted"),
                                     FieldPanel("show_in_menus"),
                                     FieldPanel('tags', heading="Tags", help_text="Tags to categorize the page"),
                                     ],
                                     heading="Site Visibility",
                                     help_text="Settings controlling how the page will show up on the site.")
                    ]
    settings_panels = Page.settings_panels

    search_fields = Page.search_fields + [index.SearchField('tags'),
                                          index.SearchField('garden_status'),
                                          index.FilterField('unlisted'),]

    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        return {}


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

    def add_interpage_links(self):
        pass

    def _add_interpage_links_from_html_field(self, html_field):
        field = getattr(self, html_field)
        soup = BeautifulSoup(str(field), 'html.parser')
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

class HomePage(AbstractPage):
    page_description = "Home page to create multi column layouts, and non-content pages."

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

    def add_interpage_links(self):
        self._add_interpage_links_from_html_field("body")

class Article(AbstractPage):
    page_description = "Article pages for long form writing and essays."

    header = StreamField(article_header_fields, use_json_field=True, null=True, blank=True)
    body = StreamField(article_fields, use_json_field=True, null=True, blank=True)

    content_panels = AbstractPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("body"),
    ]

    search_fields = AbstractPage.search_fields + [
        index.SearchField('body'),
    ]

    def get_template(self, request, *args, **kwargs):
        if request.META.get('HTTP_HX_REQUEST'):
            return "home/article_partial.html"

        return "home/article.html"

    def get_context(self, request, *args, **kwargs):
        context = super(AbstractPage, self).get_context(request, *args, **kwargs)

        series_id = request.GET.get("series")

        if series_id:
            try:
                series = Series.objects.get(id=series_id)
            except:
                series = None
        else:
            series = None

        context["series"] = series

        links = InterPageLink.objects.filter(to_page=self).exclude(from_page=self)
        links = Counter(links).most_common(4)

        context['links'] = links

        context["HTMX"] = request.META.get('HTTP_HX_REQUEST')

        print("HTMX?",context["HTMX"])

        return context

    def serve(self, request):

        # create pageview
        PageHit.objects.create(page=self)
        return super().serve(request)


    def add_interpage_links(self):
        self._add_interpage_links_from_html_field("body")


class Series(AbstractPage):
    page_description = "Series, a collection of articles."
    articles = StreamField([("articles", blocks.ListBlock(blocks.PageChooserBlock(page_type="home.Article")))],
                            use_json_field=True, null=True, blank=True)

    content_panels = AbstractPage.content_panels + [
                    FieldPanel("articles"),
            ]

    def serve(self, request):
        # add pageview
        PageHit.objects.create(page=self)

        first_article = self.articles[0].value[0]
        return redirect(f"{first_article.url}?series={self.id}")