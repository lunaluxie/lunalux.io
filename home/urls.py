from django.urls import path

from home.views import article_list, article_tag_list, project_list

urlpatterns = [
    path("articles/", article_list, name="articles-list"),
    path("articles/tag/<str:tag>", article_tag_list, name="articles-tag_list"),
    path("projects/", project_list, name="projects-list"),
]