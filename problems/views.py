from django.shortcuts import redirect, get_object_or_404, render

from problems.models import Book, Problem

def problem_detail(request, id):
    problem = get_object_or_404(Problem, id=id)


    return render(request, "problems/problem_detail.html", {"problem": problem})


def book_list(request):
    books = Book.objects.all()

    return render(request, "problems/book_list.html", {"books": books})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    return render(request, "problems/book_detail.html", {"book": book})