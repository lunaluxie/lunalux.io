from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from taggit.models import Tag

from home.filtering import filter_on_abstract_page_properties, filter_page_with_any_of_tags, filter_on_child_page_properties
from home.models.page_models import Page, Article, AbstractPage

class RSSFeed(Feed):
    def get_object(self, request, type):

        obj = {
            "type": type
        }


        garden_status = request.GET.get('garden_status')
        if garden_status:
            obj["garden_status"] = garden_status

        tags = request.GET.getlist('tags')
        if tags:
            obj['objects'] = filter_page_with_any_of_tags(tags)
            obj["tags"] = tags

        match type:
            case "timeline":
                if not tags:
                    obj['objects'] = Page.objects.live().filter(filter_on_abstract_page_properties(unlisted=False)).order_by("-first_published_at")

                if garden_status:
                    obj['objects'] = obj['objects'].filter(filter_on_abstract_page_properties(garden_status=garden_status))

                obj["link"] = "/timeline"
            case "articles":
                if tags:
                    obj['objects'] = obj['objects'].type(Article).filter(filter_on_child_page_properties(Article, article_type="article"))
                    if garden_status:
                        obj['objects'] = obj['objects'].filter(filter_on_child_page_properties(Article, garden_status=garden_status))
                else:
                    obj['objects'] = Article.objects.live().filter(unlisted=False, article_type="article").order_by("-first_published_at")
                    if garden_status:
                        obj['objects'] = obj['objects'].filter(garden_status=garden_status)

                obj["link"] = "/articles"
            case "notes":
                if tags:
                    obj['objects'] = obj['objects'].type(Article).filter(filter_on_child_page_properties(Article, article_type="note"))
                    if garden_status:
                        obj['objects'] = obj['objects'].filter(filter_on_child_page_properties(Article, garden_status=garden_status))
                else:
                    obj['objects'] = Article.objects.live().filter(unlisted=False, article_type="note").order_by("-first_published_at")
                    if garden_status:
                        obj['objects'] = obj['objects'].filter(garden_status=garden_status)

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
            categories = list(item.specific.tags.all())

            if item.specific.garden_status != "n/a":
                categories.append(item.specific.garden_status)
        else:
            categories = []

        return categories

    def item_author_name(self, item):
        return item.owner.get_full_name()

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return item.last_published_at

class AtomFeed(RSSFeed):
    feed_type = Atom1Feed

    subtitle = RSSFeed.description