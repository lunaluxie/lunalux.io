# TODO
- make body page be able to mimic article. 

How to get pages of different subclasses filtering on subclass fields.
```Python
abstract_pages = Page.objects.filter(Q(series__unlisted=False) | Q(article__unlisted=False))
abstract_pages.specific()
```

- remove unused css 
- refactor article_list. 
