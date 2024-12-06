from taggit.models import TaggedItemBase, TagBase
from treebeard.mp_tree import MP_Node
from wagtail.models import Page
from django.db import models
from modelcluster.fields import ParentalKey
from django.db.models.signals import pre_save
from django.dispatch import receiver


class HierarchicalTag (TagBase, MP_Node):
    name = models.CharField(max_length=100, unique=False, verbose_name='name')

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("name is a required parameter")


        # TODO: Detect changes & update slug when name changes
        # TODO: Update children when slug changes

        if self.slug and not self.pk:
            return super().save(*args, **kwargs)

        path = self.name.split("/")
        slugs = []
        for segment in path:
            slugs.append(self.slugify(segment))
        self.slug="/".join(slugs)

        get = lambda node_id: HierarchicalTag.objects.get(pk=node_id)
        if len(slugs) > 1:
            # add with parent
            try:
                current_parent = HierarchicalTag.objects.get(slug=slugs[0])
            except:
                # add root
                current_parent = HierarchicalTag.add_root(name=path[0], slug=slugs[0])

            for i, (name, slug) in enumerate(zip(path[1:-1], slugs[1:-1])):
                try:
                    # if path exists then get it
                    current_parent = get(current_parent.pk).get_children().get(slug="/".join(slugs[:i+2]))
                except:
                    # if path does not exist then create it
                    current_parent = get(current_parent.pk).add_child(name=name, slug="/".join(slugs[:i+2]))

            # only use 'normal' save if we are creating a new object
            if self.pk:
                result = self
                super().save(*args, **kwargs)
                self.move(get(current_parent.pk), 'last-child')
            else:
                # create leaf node
                result = get(current_parent.pk).add_child(instance=self)
        else:
            if self.pk:
                result = self
                super().save(*args, **kwargs)
                last_root = HierarchicalTag.get_last_root_node()
                self.move(last_root, 'last-sibling')
            else:
                # add as root
                result = HierarchicalTag.add_root(instance=self)

        return result




class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        Page,
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey('HierarchicalTag', related_name='%(app_label)s_%(class)s_items', on_delete=models.CASCADE)


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
