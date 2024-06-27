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

def article_list(request):
    queryset = Article.objects.all().filter(live=True, article_type="article").filter(unlisted=False)
    queryset2 = list(Series.objects.all().filter(unlisted=False))

    def time(instance):
        try:
            return instance.first_published_at
        except:
            return instance.timestamp

    queryies_combined = sorted(
        chain(queryset, queryset2),
        key=time, reverse=True)

    return render(request, "article_list.html",
                  context={"articles": queryies_combined, "tag": "all"})

def article_trending_list(request):
    articles= Article.objects.first().get_trending_articles(n=15)

    return render(request, "article_list.html",
                  context={"articles": articles, "tag": "Trending", "trending":True})




def tag_detail(request, tag):
    tag = unquote(tag)

    queryset = filter_page_with_any_of_tags(tags=[tag])

    return render(request, "article_list.html",
                  context={"articles":queryset,"tag":Tag.objects.get(slug=tag)})


def project_list(request):
    # TODO Change to single queryset on page???
    queryset = HomePage.objects.filter(live=True).filter(is_project=True)
    queryset2 = Article.objects.filter(live=True).filter(
        unlisted=False).filter(is_project=True)
    queryset3 = Series.objects.filter(live=True).filter(unlisted=False).filter(is_project=True)

    def time(instance):
        return instance.first_published_at

    queryies_combined = sorted(
        chain(queryset, queryset2, queryset3),
        key=time, reverse=True)

    return render(request, "project_list.html",
                  context={"projects":queryies_combined})