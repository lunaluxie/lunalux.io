# Generated by Django 4.0.5 on 2022-08-07 02:20

from django.db import migrations, models
import django.db.models.deletion
import home.blocks
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('home', '0003_article_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('AboutBlurb', wagtail.blocks.StructBlock([('tagline', wagtail.blocks.CharBlock()), ('column1_text', wagtail.blocks.RichTextBlock()), ('column2_text', wagtail.blocks.RichTextBlock()), ('page', wagtail.blocks.PageChooserBlock())])), ('JumbotronCard', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock())])), ('ContactForm', home.blocks.ContactForm()), ('columns', wagtail.blocks.StructBlock([('children', wagtail.blocks.ListBlock(home.blocks.ColumnBlock)), ('margin_y', wagtail.blocks.BooleanBlock(default=False, required=False)), ('margin_x', wagtail.blocks.BooleanBlock(default=False, required=False)), ('fullscreen', wagtail.blocks.BooleanBlock(default=False, required=False))])), ('spacer', home.blocks.SpacerBlock()), ('ImageHeader', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())])), ('ImageCard', wagtail.blocks.StructBlock([('header', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.blocks.CharBlock()), ('link_text', wagtail.blocks.CharBlock())])), ('text', wagtail.blocks.RichTextBlock()), ('image_card', wagtail.blocks.StructBlock([('header', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('link', wagtail.blocks.CharBlock()), ('link_text', wagtail.blocks.CharBlock())])), ('image', wagtail.images.blocks.ImageChooserBlock(template='blocks/image.html')), ('table', wagtail.contrib.table_block.blocks.TableBlock())], blank=True, null=True, use_json_field=True),
        ),
    ]
