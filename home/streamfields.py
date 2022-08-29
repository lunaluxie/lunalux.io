from wagtail.core import blocks
from wagtail.core.fields import StreamField

from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

from .blocks import *


# utility blocks
basic_fields = [
    ("text", blocks.RichTextBlock(group="basic")),
    ("image", ImageChooserBlock(template="blocks/image.html", group="basic")),
    ('table', TableBlock(group="basic")),
]

body_fields = [
    # my thing

    ("CardList", CardListBlock(group="List")),
    ("HorizontalCardList",HorizontalCardList(group="List")),
    ("LinesList",LinesListBlock(group="List")),


    ("AboutBlurb",AboutBlurb(group="")),
    ("ContactForm", ContactForm(group="")),

    # automatic
    ("recent_articles", RecentArticlesBlocks(group="automatic")),
    ("recent_projects", RecentProjectsBlocks(group="automatic")),


    # structure
    ("spacer",SpacerBlock(group="layout")),

    ("JumbotronCard",JumbotronCardBlock(group="ImageHeader")),
    ("ImageHeader", ImageHeaderBlock(group="ImageHeader")),
    ("ImageDivider", ImageDividerBlock(group="ImageHeader")),

] + basic_fields

article_fields =  basic_fields + [
    ("ImageDivider", ImageDividerBlock()),
]

article_header_fields = [
    ("ImageHeader", ImageHeaderBlock()),
    ("ImageDivider", ImageDividerBlock()),
    ("spacer", SpacerBlock()),
]