from django.urls import path

from home.views import (article_list,
                        tag_detail,
                        project_list,
                        article_trending_list,
                        notes_list,
                        timeline)

urlpatterns = [
    path("notes/", notes_list, name="notes-list"),
    path("articles/", article_list, name="articles-list"),
    path('timeline/', timeline, name='timeline'),
    path("trending/", article_trending_list, name="articles-trending-list"),
    path("tag/<str:tag>", tag_detail, name="tags-detail"),
    path("projects/", project_list, name="projects-list"),
]