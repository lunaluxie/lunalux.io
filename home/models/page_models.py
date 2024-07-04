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
from wagtail.documents import get_document_model
from taggit.models import Tag

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
        ('withering', "🍂 Withering: For outdated work where inaccuracies can accumulate and my opinions may change.")
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
                                     FieldPanel("garden_status"),
                                     FieldPanel("is_project"),
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
        context = super().get_context(request, *args, **kwargs)
        context["HTMX"] = request.META.get('HTTP_HX_REQUEST')

        return context

    def type(self):
        return self.__class__.__name__

    def get_page_type(self):
        if self.is_project:
            return "project"
        return self.type()

    def include_image_in_article_list(self):
        if self.is_project:
            return True
        if self.type()=="Series":
            return True
        else:
            return False


    def get_recent_articles(self, n=8):
        return Article.objects.all().filter(live=True, unlisted=False, article_type="article").order_by('-last_published_at')[:n]

    def get_trending_articles(self, n=8):
        """Note we get all trending article no matter which type (note or article) they are.
        The name is for historical reasons

        Args:
            n (int, optional): Number of pages to get. Defaults to 8.

        """
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
            Q(unlisted=False),
            Q(live=True),
        ).order_by(ordering)[:n]

        if not queryset_with_proper_pages:
            return self.get_recent_articles(n=n)

        return queryset_with_proper_pages

    def get_all_articles(self):
        return Article.objects.all().filter(live=True, unlisted=False, article_type="article").order_by('-last_published_at')

    def get_recent_projects(self, n=3):
        return Page.objects.all().filter(live=True).filter(is_project=True).order_by('-last_published_at').specific()[:n]

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

    def get_template(self, request, *args, **kwargs):
        if request.META.get('HTTP_HX_REQUEST'):
            return "home/home_page_partial.html"

        return "home/home_page.html"

    def add_interpage_links(self):
        self._add_interpage_links_from_html_field("body")

class Article(AbstractPage):
    page_description = "Article pages for long form writing and essays."

    header = StreamField(article_header_fields, use_json_field=True, null=True, blank=True)
    body = StreamField(article_fields, use_json_field=True, null=True, blank=True)

    choices = (
        ("article", "📕 Article: For long form writing and essays - should be worth the reader's time"),
        ("note", "📝 Note: For shorter pieces, or notes - may not be as polished as an article"),
    )
    article_type = models.CharField(max_length=100, choices=choices, default='article', help_text="Type of article, e.g. Article, Note, etc.")

    content_panels = AbstractPage.content_panels + [
        FieldPanel('article_type'),
        FieldPanel("header"),
        FieldPanel("body"),
    ]

    search_fields = AbstractPage.search_fields + [
        index.SearchField('body'),
    ]

    def get_page_type(self):
        if self.is_project:
            return "project"
        return self.article_type

    def get_template(self, request, *args, **kwargs):
        if request.META.get('HTTP_HX_REQUEST'):
            if request.GET.get("fragment")=="recommendation":
                return "components/recommendations.html"

            return "home/article_partial.html"

        return "home/article.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        series_id = request.GET.get("series")

        if series_id:
            try:
                series = Series.objects.get(id=series_id)
            except:
                series = None
        else:
            series = None

        context["series"] = series

        if request.GET.get("fragment")=="recommendation":
            links = InterPageLink.objects.filter(to_page=self).select_related("from_page").exclude(from_page=self)
            links = links.filter(from_page__live=True)
            links = [obj.from_page.specific for obj, freq in Counter(links).most_common(4) if not obj.from_page.specific.unlisted]
            context['links'] = links

            context['similar_objects'] = self.tags.similar_objects()[:10]

            link_ids = [obj.id for obj in links]
            context['similar_objects'] = [obj.specific for obj in context['similar_objects']
                                        if obj.specific.live
                                            and not obj.specific.unlisted
                                            and obj.id not in  link_ids]

            # TODO: Make it count all page types not just articles.
            tags = Tag.objects.all().annotate(
                num_times=Count('home_pagetag_items')
            ).filter(article=self).order_by('-num_times')
            context['tags'] = tags

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

    def add_interpage_links(self):
        for article in self.articles:
            for a in article.value:
                interlink = InterPageLink.objects.get_or_create(from_page=self, to_page=a)


class DocumentPage(Page):
    page_description = "Document page only for giving documents a permanent url."

    document = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    content_panels = Page.content_panels + [
        FieldPanel("document"),
    ]

    def serve(self, request, *args, **kwargs):
        return redirect(self.document.url)
