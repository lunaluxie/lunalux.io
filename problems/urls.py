from django.urls import path

from problems.views import problem_detail, book_detail, book_list

urlpatterns = [
    path("<int:id>/", problem_detail, name="problem_detail"),
    path("books/", book_list, name="book_list"),
    path("books/<int:id>/", book_detail, name="book_detail"),
]