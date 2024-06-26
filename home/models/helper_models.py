from taggit.models import TaggedItemBase
from wagtail.models import Page
from django.db import models
from modelcluster.fields import ParentalKey


class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        Page,
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class InterPageLink(models.Model):
    from_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="from_page_related")
    to_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="to_page_related")


class PageHit(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.page.title} - {self.timestamp}"


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    message = models.TextField()

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
