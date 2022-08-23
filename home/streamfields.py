from .blocks import (HorizontalCardList,
                    LinesListBlock,
                    JumbotronCardBlock,
                    CardListBlock,
                    ContactForm,
                    ImageHeaderBlock,
                    ImageDividerBlock,
                    ImageCardBlock,
                    SpacerBlock,
                    ColumnBlock,
                    ColumnsBlock,
                    basic_fields,
                    AboutBlurb)
from wagtail.core.fields import StreamField

body_fields = [
    # my thing
    ("AboutBlurb",AboutBlurb()),
    ("JumbotronCard",JumbotronCardBlock()),
    ("CardList", CardListBlock()),
    ("LinesList",LinesListBlock()),
    ("ContactForm", ContactForm()),


    # structure
    ("columns", ColumnsBlock()),
    ("spacer",SpacerBlock()),

    # GI
    ("ImageHeader", ImageHeaderBlock()),
    ("ImageDivider", ImageDividerBlock()),
    ("ImageCard",ImageCardBlock()),

] + basic_fields

article_fields =  basic_fields + [
    ("ImageHeader", ImageHeaderBlock()),
    ("ImageDivider", ImageDividerBlock()),
]

article_header_fields = [
    ("ImageHeader", ImageHeaderBlock()),
    ("ImageDivider", ImageDividerBlock()),
]