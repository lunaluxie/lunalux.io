from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

# BASIC BLOCKS

class CodeBlock(blocks.StructBlock):
    choices = (
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('bash', 'Bash'),
        ('plaintext', 'Plain text'),
    )
    language = blocks.ChoiceBlock(required=True, choices=choices, default='plaintext')
    code = blocks.TextBlock()

    class Meta:
        icon = "code"
        template = "blocks/code_block.html"

class DescriptionBlock(blocks.StructBlock):
    text = blocks.TextBlock()

    class Meta:
        icon = "pilcrow"
        template = "blocks/description_block.html"

# SECTION BLOCKS?

class AlertBlock(blocks.StructBlock):
    body = blocks.RichTextBlock()
    icon = blocks.CharBlock(required=False, max_length=2)

    choices = (
        ("info","Info"),
        ("warning","Warning"),
        ("danger","Danger"),
        ("success","Success")
    )
    style = blocks.ChoiceBlock(choices=choices, default="info")

    class Meta:
        icon = "warning"
        template = "blocks/alert.html"

class CardListBlock(blocks.StructBlock):

    pages = blocks.ListBlock(
        blocks.PageChooserBlock())

    title = blocks.CharBlock(required=False)

    hide_link = blocks.BooleanBlock(required=False, default=False)

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
    title = blocks.CharBlock(required=False)
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
        admin_text = 'configured elsewhere'
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

### META BLOCKS

class ContainerBlock(blocks.StructBlock):
    content = blocks.StreamBlock([
        # structure
        ("spacer", SpacerBlock(group="layout")),

        ("text", blocks.RichTextBlock(group="basic")),
        ("image", ImageChooserBlock(template="blocks/image.html", group="basic")),
        ('table', TableBlock(group="basic")),

    ])

    class Meta:
        template = "blocks/container.html"
        help_text = "Creates a container for text and images. Useful if you want the proper margin for wide-page layouts."
        label = 'Container: (Use this for text in wide layouts)'


class ColumnBlock(blocks.StructBlock):
    content = blocks.StreamBlock([
        ("text", blocks.RichTextBlock(group="basic")),
        ("image", ImageChooserBlock(template="blocks/image.html", group="basic")),
        ('table', TableBlock(group="basic")),

        ("lines_list", LinesListBlock(group="components")),
        ('horizontal_card_list', HorizontalCardList(group="components")),
    ])

    class Meta:
        template = "blocks/column.html"
        help_text = "Creates a column."
        label = 'Column (add another column)'

class ColumnsBlock(blocks.StructBlock):
    columns = blocks.StreamBlock([
        ("column", ColumnBlock())
    ])

    class Meta:
        template = "blocks/columns.html"
        help_text = "Create multi column layouts."
        label = 'Columns: (Use this for multi-column layouts)'

class CenteredTextContentBlock(blocks.StructBlock):
    body = blocks.StreamBlock([
        ("text", blocks.RichTextBlock(group="basic")),
        ("image", ImageChooserBlock(template="blocks/image.html", group="basic")),
        ('table', TableBlock(group="basic")),
        ('code', CodeBlock(group="basic")),
        ('alert', AlertBlock(group="basic")),
    ])

    class Meta:
        template = "blocks/centered_text_content.html"
        help_text = "Creates a centered text content block. (like in article)"
        label = 'Centered Text Content: (Use this for to mimic article text layout)'