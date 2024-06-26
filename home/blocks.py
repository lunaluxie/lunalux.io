from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

# BASIC BLOCKS

class CodeBlock(blocks.StructBlock):
    language = blocks.CharBlock(required=False)
    code = blocks.TextBlock()

    class Meta:
        icon = "code"
        template = "blocks/code_block.html"

# SECTION BLOCKS?

class CardListBlock(blocks.StructBlock):

    pages = blocks.ListBlock(
        blocks.PageChooserBlock())

    class Meta:
        # icon = ""
        label = "Card list (project list)"
        admin_text = 'project list.'
        template = 'blocks/card_list.html'

class HorizontalCardList(blocks.StructBlock):

    pages = blocks.ListBlock(
        blocks.PageChooserBlock())

    class Meta:
        # icon = ""
        label = "Horizontal card list (about)"
        admin_text = 'about card list.'
        template = 'blocks/horizontal_card_list.html'

class LinesListBlock(blocks.StructBlock):

    pages = blocks.ListBlock(blocks.PageChooserBlock(
        target_model=["home.HomePage","home.Article"]))

    include_images = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        # icon = ""
        label = ""
        admin_text = 'Line list with images.'
        template = 'blocks/lines_list.html'

class JumbotronCardBlock(blocks.StructBlock):

    jumbotron = blocks.PageChooserBlock()

    class Meta:
        # icon = ""
        label = "Jumbotron card block"
        admin_text = 'header on start site'
        template = 'blocks/jumbotron_card.html'

class JumbotronImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        # icon = ""
        label = "Jumbotron image block"
        admin_text = 'header on start site'
        template = 'blocks/jumbotron_image.html'



class RecentArticlesBlocks(blocks.StructBlock):
    number_of_articles = blocks.IntegerBlock(min_value=1, default=5)

    class Meta:
        # icon = ""
        label = ""
        admin_text = ''
        template = 'blocks/recent_articles.html'


class TrendingArticlesBlock(blocks.StructBlock):
    number_of_articles = blocks.IntegerBlock(min_value=1, default=5)

    class Meta:
        # icon = ""
        label = "Trending Articles"
        admin_text = ''
        template = 'blocks/trending_articles.html'


class RecentProjectsBlocks(blocks.StructBlock):
    number_of_projects = blocks.IntegerBlock(min_value=1, default=3)

    class Meta:
        # icon = ""
        label = ""
        admin_text = ''
        template = 'blocks/recent_projects.html'



# PAGE BLOCKS

class AllProjectsBlocks(blocks.StaticBlock):
    class Meta:
        # icon = ""
        label = ""
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'blocks/all_projects.html'



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


# LAYOUT

class SpacerBlock(blocks.StaticBlock):
    class Meta:
        icon = ""
        label = "Create a y-margin spacer"
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'blocks/spacer.html'


class NavMarginBlock(blocks.StaticBlock):
    class Meta:
        icon = ""
        label = "Create a 55px invisible element to skip header"
        admin_text = '{label}: configured elsewhere'.format(label=label)
        template = 'blocks/navmarginblock.html'



class ImageHeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    image = ImageChooserBlock()

    large = blocks.BooleanBlock(default=False, required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_header.html"


class ImageDividerBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = "image"
        template = "blocks/image_divider.html"


class ContainerBlock(blocks.StructBlock):
    content = blocks.StreamBlock([
        # my thing
        ("CardList", CardListBlock(group="List")),
        ("HorizontalCardList", HorizontalCardList(group="List")),
        ("LinesList", LinesListBlock(group="List")),


        ("AboutBlurb", AboutBlurb(group="")),
        ("ContactForm", ContactForm(group="")),

        # automatic
        ("recent_articles", RecentArticlesBlocks(group="automatic")),
        ("recent_projects", RecentProjectsBlocks(group="automatic")),


        # structure
        ("spacer", SpacerBlock(group="layout")),

        ("JumbotronCard", JumbotronCardBlock(group="ImageHeader")),
        ("ImageHeader", ImageHeaderBlock(group="ImageHeader")),
        ("ImageDivider", ImageDividerBlock(group="ImageHeader")),

        ("text", blocks.RichTextBlock(group="basic")),
        ("image", ImageChooserBlock(template="blocks/image.html", group="basic")),

    ])

    class Meta:
        template = "blocks/container.html"
