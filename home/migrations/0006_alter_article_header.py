# Generated by Django 4.0.7 on 2023-02-11 10:34

from django.db import migrations
import home.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_series_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='header',
            field=wagtail.fields.StreamField([('JumbotronImageBlock', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('ImageHeader', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('large', wagtail.blocks.BooleanBlock(default=False, required=False))])), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())])), ('spacer', home.blocks.SpacerBlock()), ('skipNavMargin', home.blocks.NavMarginBlock())], blank=True, null=True, use_json_field=True),
        ),
    ]
