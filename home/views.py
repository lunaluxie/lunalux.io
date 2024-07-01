from django.shortcuts import render
from itertools import chain
from urllib.parse import unquote
import datetime
from django.utils import timezone
from collections import Counter
from home.models.page_models import Page, AbstractPage, HomePage, Article, Series
from home.models.helper_models import PageHit, PageTag
from home.filtering import filter_on_abstract_page_properties, filter_page_with_any_of_tags
from taggit.models import Tag

def garden_list(request):

    garden_status = request.GET.get('garden_status')

    # TODO Change to single queryset on page???
    queryset = HomePage.objects.filter(live=True, unlisted=False).exclude(garden_status='na')
    queryset2 = Article.objects.filter(live=True, unlisted=False).exclude(garden_status='na')
    queryset3 = Series.objects.filter(live=True, unlisted=False).exclude(garden_status='na')

    if garden_status:
        queryset = queryset.filter(garden_status=garden_status)
        queryset2 = queryset2.filter(garden_status=garden_status)
        queryset3 = queryset3.filter(garden_status=garden_status)

    def time(instance):
        return instance.last_published_at

    queryies_combined = sorted(
        chain(queryset, queryset2, queryset3),
        key=time, reverse=True)

    context = {"articles": queryies_combined, "tag": "Garden", 'hide_other_tags':True, "show_garden_status":True, "object_name": "Pages"}

    context['description_text'] = "A collection of pages on various topics."

    # TODO: Don't use article_list template for garden view
    # in general move away from exclusively using article_list template
    return render(request, "article_list.html",
                  context=context)


def timeline(request):
    # TODO Change to single queryset on page???
    queryset = HomePage.objects.filter(live=True, unlisted=False)
    queryset2 = Article.objects.filter(live=True, unlisted=False)
    queryset3 = Series.objects.filter(live=True, unlisted=False)

    def time(instance):
        return instance.last_published_at

    queryies_combined = sorted(
        chain(queryset, queryset2, queryset3),
        key=time, reverse=True)

    context = {"articles": queryies_combined, "tag": "Timeline", 'hide_other_tags':True, "object_name": "Pages"}

    context['description_text'] = "A chronological list of all pages."

    return render(request, "article_list.html",
                  context=context)

def notes_list(request):
    queryset = Article.objects.all().filter(live=True, article_type="note").filter(unlisted=False).order_by("-first_published_at")

    context = {"articles": queryset, "tag": "Notes", 'hide_other_tags':True, "object_name": "Notes"}

    context['description_text'] = "A collection of notes on various topics."

    return render(request, "article_list.html",
                  context=context)

def article_list(request):
    queryset = Article.objects.all().filter(live=True, article_type="article").filter(unlisted=False)
    queryset2 = Series.objects.live().filter(unlisted=False)

    def time(instance):
        try:
            return instance.first_published_at
        except:
            return instance.timestamp

    queryies_combined = sorted(
        chain(queryset, queryset2),
        key=time, reverse=True)

    tags = Article.tags.most_common().exclude(slug__in=['ai', 'physics'])[:10]

    return render(request, "article_list.html",
                  context={"articles": queryies_combined, "tag": "all", 'tags':tags, "object_name": "Essays"})

def article_trending_list(request):
    articles= Article.objects.first().get_trending_articles(n=15)

    return render(request, "article_list.html",
                  context={"articles": articles, "tag": "Trending", "trending":True, "object_name": "Items"})

def tag_detail(request, tag):
    tag = unquote(tag)

    queryset = filter_page_with_any_of_tags(tags=[tag])

    context = {"articles":queryset,
               "object_name": "Items",
               "tag":Tag.objects.get(slug=tag)}

    if request.GET.get('hide_other_tags'):
        context["hide_other_tags"] = True

    return render(request, "article_list.html",
                  context=context)


def project_list(request):
    # TODO Change to single queryset on page???
    queryset = HomePage.objects.filter(live=True, unlisted=False).filter(is_project=True)
    queryset2 = Article.objects.filter(live=True, unlisted=False).filter(is_project=True)
    queryset3 = Series.objects.filter(live=True, unlisted=False).filter(is_project=True)

    def time(instance):
        return instance.first_published_at

    queryies_combined = sorted(
        chain(queryset, queryset2, queryset3),
        key=time, reverse=True)

    return render(request, "project_list.html",
                  context={"projects":queryies_combined})