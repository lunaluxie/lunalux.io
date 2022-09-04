from django import template
register = template.Library()

from home.models import HomePage, Article, Series

@register.simple_tag
def define(val=None):
  print(dir(val[0]))
  return val


@register.simple_tag
def pageChooserBlockListToProperPages(val=None):

  pageids = []

  for v in val:
    pageids.append(v.id)

  pages = []
  for i in pageids:

    try:
      pages.append(HomePage.objects.get(id=i))
    except:
      try:
        pages.append(Article.objects.get(id=i))
      except:
        pages.append(Series.objects.get(id=i))

  return pages


@register.simple_tag
def pageToProperPage(val=None):

  try:
    page = HomePage.objects.get(id=val.id)
  except:
    page = Article.objects.get(id=val.id)
  return page
