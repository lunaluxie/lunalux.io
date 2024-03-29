from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from home.models import AbstractPage, Article,Series
from wagtail.search.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)

        pages = []
        for page in search_results:
            try:
                pages.append(Article.objects.get(id=page.id))
            except: pass
            try:
                pages.append(Series.objects.get(id=page.id))
            except: pass

        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        pages = Article.objects.live().order_by('-first_published_at')
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    if not search_query:
        search_query=""

    return TemplateResponse(
        request,
        "article_list.html",
        {
            "search_query": search_query,
            "articles": pages,
            "is_search": True
        },
    )
