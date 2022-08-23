from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class CardListBlock(blocks.StructBlock):
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    class Meta:
        # icon = ""
        label = "Card list (project list)"
        admin_text = 'project list.'
        template = 'blocks/card_list.html'

class HorizontalCardList(blocks.StructBlock):
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    class Meta:
        # icon = ""
        label = "Horizontal card list (about)"
        admin_text = 'about card list.'
        template = 'blocks/horizontal_card_list.html'

class LinesListBlock(blocks.StructBlock):
    pages = blocks.ListBlock(blocks.PageChooserBlock())

    include_images = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        # icon = ""
        label = ""
        admin_text = 'Line list with images.'
        template = 'blocks/lines_list.html'

class JumbotronCardBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock()

    class Meta:
        # icon = ""
        label = "Jumbotron card block"
        admin_text = 'header on start site'
        template = 'blocks/jumbotron_card.html'


class RecentArticlesBlocks(blocks.StructBlock):
    number_of_articles = blocks.IntegerBlock(min_value=1, default=5)

    class Meta:
        # icon = ""
        label = ""
        admin_text = ''
        template = 'blocks/recent_articles.html'


class RecentProjectsBlocks(blocks.StructBlock):
    number_of_projects = blocks.IntegerBlock(min_value=1, default=3)

    class Meta:
        # icon = ""
        label = ""
        admin_text = ''
        template = 'blocks/recent_projects.html'


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


class SpacerBlock(blocks.StaticBlock):
    class Meta:
        icon = ""
        label = "Create a y-margin spacer"
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'blocks/spacer.html'



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
