from tokenize import group
from wagtail import blocks
from wagtail.fields import StreamField

from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from .blocks import *
from .oneoff_blocks import *

# utility blocks
basic_fields = [
    ("text", blocks.RichTextBlock(group="basic")),
    ("image", ImageChooserBlock(template="blocks/image.html", group="basic")),
    ('table', TableBlock(group="basic")),
    ("code", CodeBlock(group="basic")),
]

body_fields = [
    # my thing
    ("CardList", CardListBlock(group="List")),
    ("HorizontalCardList",HorizontalCardList(group="List")),
    ("LinesList",LinesListBlock(group="List")),


    ("AboutBlurb",AboutBlurb(group="")),
    ("ContactForm", ContactForm(group="")),

    # automatic
    ("trending_articles", TrendingArticlesBlock(group="automatic")),
    ("recent_articles", RecentArticlesBlocks(group="automatic")),
    ("recent_projects", RecentProjectsBlocks(group="automatic")),


    # structure
    ("spacer",SpacerBlock(group="layout")),
    ("container", ContainerBlock(group="layout")),
    ('columns', ColumnsBlock(group="layout")),
    ("skipNavMargin", NavMarginBlock(group="layout")),

    # headers
    ("JumbotronImageBlock", JumbotronImageBlock(group="ImageHeader")),
    ("JumbotronCard",JumbotronCardBlock(group="ImageHeader")),
    ("ImageHeader", ImageHeaderBlock(group="ImageHeader")),
    ("ImageDivider", ImageDividerBlock(group="ImageHeader")),

]

article_fields =  basic_fields + [
    ("ImageDivider", ImageDividerBlock()),

    ("GradientDescentWidget", GradientDescentWidget(group="oneoff")),
    ("StatisticalMurderWidget", StatisticalMurderWidget(group="oneoff")),
    ("IRTWidget", IRTWidget(group="oneoff")),
    ("WealthEnergyWidget", WealthEnergyWidget(group="oneoff")),
]

article_header_fields = [
    ("JumbotronImageBlock", JumbotronImageBlock(group="ImageHeader")),
    ("ImageHeader", ImageHeaderBlock()),
    ("ImageDivider", ImageDividerBlock()),
    ("spacer", SpacerBlock()),
    ("skipNavMargin", NavMarginBlock()),
]