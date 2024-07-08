from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from home.filtering import filter_on_abstract_page_properties

from taggit.models import Tag

from home.models.page_models import Page, Article, AbstractPage

class RSSFeed(Feed):
    def get_object(self, request, type):

        obj = {
            "type": type
        }

        match type:
            case "timeline":
                obj['objects'] = Page.objects.live().filter(filter_on_abstract_page_properties(unlisted=False)).order_by("-first_published_at")
                obj["link"] = "/timeline"
            case "articles":
                obj['objects'] = Article.objects.live().filter(unlisted=False, article_type="article")#.order_by("-first_published_at")
                obj["link"] = "/articles"
            case "notes":
                obj['objects'] = Article.objects.live().filter(unlisted=False, article_type="note").order_by("-first_published_at")
                obj["link"] = "/notes"

        return obj

    def title(self, obj):
        return f"Luna Lux - {obj['type']}"

    def description(self, obj):
        return f"Additions to {obj['type']}."

    def link(self, obj):
        return obj["link"]

    def items(self, obj):
        return obj['objects']

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.search_description

    def item_link(self, item):
        return item.get_full_url()

    def item_categories(self, item):
        if isinstance(item.specific, AbstractPage):
            return list(item.specific.tags.all())
        else:
            return []

    def item_author_name(self, item):
        return item.owner.get_full_name()

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return item.last_published_at

class AtomFeed(RSSFeed):
    feed_type = Atom1Feed

    subtitle = RSSFeed.description