from django.urls import path

from home.views import (article_list,
                        tag_detail,
                        project_list,
                        article_trending_list,
                        notes_list,
                        timeline,
                        garden_list,
                        hover_preview,
                        feed_preview)

from home.feeds import RSSFeed, AtomFeed

urlpatterns = [
    path("notes/", notes_list, name="notes-list"),
    path("articles/", article_list, name="articles-list"),
    path('garden/', garden_list, name='garden-list'),
    path('timeline/', timeline, name='timeline'),
    path("trending/", article_trending_list, name="articles-trending-list"),
    path("tag/<str:tag>", tag_detail, name="tags-detail"),
    path("projects/", project_list, name="projects-list"),
    path("hover-preview/", hover_preview, name="hover-preview"),

    # feeds
    path('feeds/preview', feed_preview, name="feed-preview"),
    path("feeds/rss/<str:type>/", RSSFeed(), name="rss-feed"),
    path("feeds/atom/<str:type>/", AtomFeed(), name="atom-feed"),
]