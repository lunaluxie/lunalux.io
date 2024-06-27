from django.db.models import Q
from wagtail.models import Page
from home.models.page_models import AbstractPage
from home.models.helper_models import PageTag



abstract_page_subclasses = AbstractPage.__subclasses__()

def filter_on_abstract_page_properties(**filtering_params) -> Q:
    """
    Filter on the property of an AbstractPage.

    Only supports equality filtering.

    Example:

    ```
    Page.objects.type(AbstractPage).filter(filter_on_abstract_page_properties(is_project=True))
    ```
    """
    # Build the dynamic Q object for filtering
    query = Q()

    for key, value in filtering_params.items():
        for subclass in abstract_page_subclasses:
            model_name = subclass._meta.model_name
            query |= Q(**{f"{model_name}__{key}": value})

    return query


def filter_page_with_any_of_tags(tags):
    queryset = PageTag.objects.filter(tag__slug__in=tags)
    page_ids = queryset.filter(content_object__live=True).values_list('content_object__id', flat=True)

    queryset = Page.objects.type(AbstractPage).filter(id__in=page_ids)
    queryset = queryset.filter(filter_on_abstract_page_properties(unlisted=False))
    queryset = queryset.distinct().order_by('-first_published_at').specific()
    return queryset