from django.urls import path

from home.views import article_list, tag_detail, project_list, article_trending_list

urlpatterns = [
    path("articles/", article_list, name="articles-list"),
    path("trending/", article_trending_list, name="articles-trending-list"),
    path("tag/<str:tag>", tag_detail, name="tags-detail"),
    path("projects/", project_list, name="projects-list"),
]