from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock


class HorizontalCardList(blocks.ListBlock):
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    class Meta:
        # icon = ""
        label = ""
        admin_text = 'project list.'
        template = 'blocks/horizontal_card_list.html'

class LinesListBlock(blocks.StructBlock):
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    include_images = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        # icon = ""
        label = ""
        admin_text = 'project list.'
        template = 'blocks/lines_list.html'

class JumbotronCardBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()

    class Meta:
        # icon = ""
        label = ""
        admin_text = 'header on start site'
        template = 'blocks/jumbotron_card.html'

class CardListBlock(blocks.StructBlock):
    # project list
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    class Meta:
        # icon = ""
        label = ""
        admin_text = 'project list.'
        template = 'blocks/card_list.html'

class RecentArticlesBlocks(blocks.StructBlock):
    number_of_articles = blocks.IntegerBlock(min_value=1, default=5)

    class Meta:
        # icon = ""
        label = ""
        admin_text = ''
        template = 'blocks/recent_articles.html'

class ContactForm(blocks.StaticBlock):
    class Meta:
        # icon = ""
        label = ""
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'blocks/contact_form.html'

class AboutBlurb(blocks.StructBlock):
    tagline = blocks.CharBlock()

    column1_text = blocks.RichTextBlock()
    column2_text = blocks.RichTextBlock()

    page = blocks.PageChooserBlock()

    class Meta:
        # icon = ""
        label = ""
        admin_text = ''
        template = 'blocks/about_blurb.html'

# article blocks


# GI blocks
class ImageHeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()

    class Meta:
        icon = "image"
        template = "blocks/image_header.html"


class ImageDividerBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"
        template = "blocks/image_divider.html"


class ImageCardBlock(blocks.StructBlock):
    header = blocks.CharBlock()
    description = blocks.CharBlock()

    image = ImageChooserBlock()
    link = blocks.CharBlock()
    link_text = blocks.CharBlock()

    class Meta:
        icon = "image"
        template = "blocks/image_card.html"


class SpacerBlock(blocks.StaticBlock):
    class Meta:
        icon = ""
        label = "Create a y-margin spacer"
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'blocks/spacer.html'


# utility blocks
basic_fields = [
    ("text", blocks.RichTextBlock()),
    ("image", ImageChooserBlock(template="blocks/image.html")),
    ('table', TableBlock()),
]

class ColumnBlock(blocks.StructBlock):
    content = blocks.StreamBlock(basic_fields+[('image_card', ImageCardBlock())])

    class Meta:
        icon = "placeholder"


class ColumnsBlock(blocks.StructBlock):
    children = blocks.ListBlock(ColumnBlock)

    margin_y = blocks.BooleanBlock(default=False, required=False)
    margin_x = blocks.BooleanBlock(default=False, required=False)
    fullscreen = blocks.BooleanBlock(default=False, required=False)

    class Meta:
        icon = "grip"
        template = "blocks/columns.html"