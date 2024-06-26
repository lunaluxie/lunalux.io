from django.db.models import Q
from wagtail.models import Page
from home.models.page_models import AbstractPage


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
