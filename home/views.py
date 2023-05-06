from django.shortcuts import render
from itertools import chain
from urllib.parse import unquote
import datetime
from django.utils import timezone
from collections import Counter
from .models import AbstractPage, HomePage, Article, Series, PageHit

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
    # highest number of hits in the last 7 days
    queryset = PageHit.objects.all().order_by('-timestamp').filter(page__live=True)
    queryset.filter(timestamp__gte=timezone.now() - datetime.timedelta(days=7))

    queryset = [x.page for x in queryset]
    queryset = [x[0] for x in Counter(queryset).most_common()]

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

    return render(request, "article_list.html",
                  context={"articles": queryset_with_proper_pages, "tag": "Trending", "trending":True})




def article_tag_list(request, tag):
    tag = unquote(tag)
    queryset = Article.objects.all().filter(live=True).filter(
        unlisted=False).filter(tags__name__icontains=tag).distinct().order_by('-first_published_at')

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