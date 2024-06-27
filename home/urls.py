from django.urls import path

from home.views import article_list, article_tag_list, project_list, article_trending_list

urlpatterns = [
    path("articles/", article_list, name="articles-list"),
    path("trending/", article_trending_list, name="articles-trending-list"),
    path("tag/<str:tag>", article_tag_list, name="tags-detail"),
    path("projects/", project_list, name="projects-list"),
]