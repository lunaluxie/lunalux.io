from django.db import models

# Create your models here.
from wagtail.fields import StreamField, RichTextField
from home.streamfields import article_fields

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
        FieldPanel('authors'),
    ]

    def __str__(self):
        return self.title


@register_snippet
class Problem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True, related_name='problems')

    identifier = models.CharField(max_length=255, null=True, blank=True)

    question = RichTextField(null=True, blank=True)
    answer = StreamField(article_fields, use_json_field=True, null=True, blank=True)

    panels = [
        FieldPanel('book'),
        FieldPanel('identifier'),
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    def __str__(self):
        return self.book.title + " " + self.identifier