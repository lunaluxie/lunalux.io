from django.shortcuts import render
from itertools import chain
from urllib.parse import unquote
import datetime
from django.utils import timezone
from collections import Counter
from home.models.page_models import AbstractPage, HomePage, Article, Series
from home.models.helper_models import PageHit, PageTag

def article_list(request):
    queryset = Article.objects.all().filter(live=True).filter(unlisted=False)

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




def article_tag_list(request, tag):
    tag = unquote(tag)
    # queryset = Article.objects.all().filter(live=True).filter(
    #     unlisted=False).filter(tags__name__icontains=tag).distinct().order_by('-first_published_at')

    queryset = PageTag.objects.filter(tag__name__icontains=tag).filter(content_object__live=True).filter(content_object__unlisted=False)
    queryset = queryset.distinct().order_by('-content_object__first_published_at')
    queryset = [x.content_object for x in queryset]

    return render(request, "article_list.html",
                  context={"articles":queryset,"tag":tag.lower()})


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