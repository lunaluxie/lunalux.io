from django.shortcuts import render
from itertools import chain
from .models import AbstractPage, HomePage, Article, Series

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


def article_tag_list(request, tag):
    queryset = Article.objects.all().filter(live=True).filter(
        unlisted=False).filter(tags__name__icontains=tag).distinct()

    return render(request, "article_list.html",
                  context={"articles":queryset,"tag":tag.lower()})

#.filter(is_project=True)

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