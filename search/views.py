from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.template.response import TemplateResponse
from wagtail.models import Page
from wagtail.search.backends import get_search_backend

from home.filtering import filter_on_abstract_page_properties
from home.models.page_models import AbstractPage, Article, Series


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        # TODO: Investigate searching across all page types efficiently.
        # problem now is that I cannot filter on the abstract page properties
        search_results = get_search_backend().search(search_query, Article.objects.filter(unlisted=False).live())
    else:
        search_results = (
            Article.objects.filter(unlisted=False)
            .live()
            .order_by(Coalesce("go_live_at", "first_published_at")).reverse()
        )

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

    return render(
        request,
        "article_list.html",
        {
            "search_query": search_query,
            "articles": search_results,
            "is_search": True,
            "description_text": "Can (currently) only search Notes and Essays",
            "object_name": "Search",
        },
    )
