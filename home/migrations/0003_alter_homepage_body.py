# Generated by Django 4.0.7 on 2022-08-28 17:08

from django.db import migrations
import home.blocks
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_article_body_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('CardList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock()))], group='List')), ('HorizontalCardList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock()))], group='List')), ('LinesList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock())), ('include_images', wagtail.blocks.BooleanBlock(default=True, required=False))], group='List')), ('AboutBlurb', wagtail.blocks.StructBlock([('tagline', wagtail.blocks.CharBlock()), ('column1_text', wagtail.blocks.RichTextBlock()), ('column2_text', wagtail.blocks.RichTextBlock()), ('page', wagtail.blocks.PageChooserBlock())], group='')), ('ContactForm', home.blocks.ContactForm(group='')), ('recent_articles', wagtail.blocks.StructBlock([('number_of_articles', wagtail.blocks.IntegerBlock(default=5, min_value=1))], group='automatic')), ('recent_projects', wagtail.blocks.StructBlock([('number_of_projects', wagtail.blocks.IntegerBlock(default=3, min_value=1))], group='automatic')), ('spacer', home.blocks.SpacerBlock(group='layout')), ('JumbotronCard', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock())], group='ImageHeader')), ('ImageHeader', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('ImageCard', wagtail.blocks.StructBlock([('header', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.blocks.CharBlock()), ('link_text', wagtail.blocks.CharBlock())], group='ImageHeader')), ('text', wagtail.blocks.RichTextBlock(group='basic')), ('image', wagtail.images.blocks.ImageChooserBlock(group='basic', template='blocks/image.html')), ('table', wagtail.contrib.table_block.blocks.TableBlock(group='basic'))], blank=True, null=True, use_json_field=True),
        ),
    ]
