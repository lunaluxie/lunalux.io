from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from problems.models import Problem, Book

class BookAdmin(SnippetViewSet):
    model = Book
    menu_label = 'Books'
    menu_name = 'books'
    icon = 'doc-full-inverse'
    list_display = ('title', 'authors')
    list_filter = ('title', 'authors')
    search_fields = ('title', 'authors')

class ProblemAdmin(SnippetViewSet):
    model = Problem
    menu_label = 'Problems'
    menu_name = 'problems'
    icon = 'doc-empty'
    list_display = ('book', 'identifier')
    list_filter = ('book', 'identifier')
    search_fields = ('book', 'identifier')


class ProblemsViewSetGroup(SnippetViewSetGroup):
    items = (BookAdmin, ProblemAdmin)
    menu_icon = "folder-inverse"
    menu_label = "Solved Problems"
    menu_name = "solved-problems"
    menu_order = 400  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_admin_menu = True

register_snippet(ProblemsViewSetGroup)