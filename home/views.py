from django.shortcuts import render
from .models import AbstractPage, HomePage, Article

def article_list(request):
    queryset = Article.objects.all().filter(live=True)

    return render(request, "article_list.html",
                  context={"articles":queryset,"tag":"all"})


def article_tag_list(request, tag):
    queryset = Article.objects.all().filter(live=True).filter(tags__name__icontains=tag).distinct()

    return render(request, "article_list.html",
                  context={"articles":queryset,"tag":tag.lower()})

#.filter(is_project=True)