from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from home.models.page_models import AbstractPage, Article,Series
from home.filtering import filter_on_abstract_page_properties

from wagtail.search.backends import get_search_backend


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = get_search_backend().search(search_query, Article.objects.filter(unlisted=False).live())
    else:
        search_results = Article.objects.filter(unlisted=False).live().order_by('-first_published_at')

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

    if request.META.get('HTTP_HX_REQUEST'):
        return TemplateResponse(
            request,
            "blocks/lines_list.html",
            {
                "search_query": search_query,
                "pages": search_results,
                "is_search": True,
                "include_images":True,
                "link_to_blog":False,
                "htmx":True,
            },
        )

    return TemplateResponse(
        request,
        "article_list.html",
        {
            "search_query": search_query,
            "articles": search_results,
            "is_search": True
        },
    )
