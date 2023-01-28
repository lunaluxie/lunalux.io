# Generated by Django 4.0.7 on 2023-01-28 14:16

from django.db import migrations
import home.blocks
import home.oneoff_blocks
import modelcluster.contrib.taggit
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_article_body_alter_article_header_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.PageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(group='basic')), ('image', wagtail.images.blocks.ImageChooserBlock(group='basic', template='blocks/image.html')), ('table', wagtail.contrib.table_block.blocks.TableBlock(group='basic')), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.blocks.TextBlock(identifier='code', label='Code'))], group='basic', label='Code')), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())])), ('GradientDescentWidget', wagtail.blocks.StructBlock([], group='oneoff')), ('StatisticalMurderWidget', home.oneoff_blocks.StatisticalMurderWidget(group='oneoff')), ('IRTWidget', home.oneoff_blocks.IRTWidget(group='oneoff')), ('WealthEnergyWidget', home.oneoff_blocks.WealthEnergyWidget(group='oneoff'))], blank=True, null=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='header',
            field=wagtail.fields.StreamField([('JumbotronImageBlock', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('ImageHeader', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('large', wagtail.blocks.BooleanBlock(default=False, required=False))])), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())])), ('spacer', home.blocks.SpacerBlock()), ('skipNavMargin', home.blocks.NavMarginBlock())], blank=True, null=True, use_json_field=None),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('CardList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock()))], group='List')), ('HorizontalCardList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock()))], group='List')), ('LinesList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.HomePage', 'home.Article']))), ('include_images', wagtail.blocks.BooleanBlock(default=True, required=False))], group='List')), ('AboutBlurb', wagtail.blocks.StructBlock([('tagline', wagtail.blocks.CharBlock()), ('column1_text', wagtail.blocks.RichTextBlock()), ('column2_text', wagtail.blocks.RichTextBlock()), ('page', wagtail.blocks.PageChooserBlock())], group='')), ('ContactForm', home.blocks.ContactForm(group='')), ('recent_articles', wagtail.blocks.StructBlock([('number_of_articles', wagtail.blocks.IntegerBlock(default=5, min_value=1))], group='automatic')), ('recent_projects', wagtail.blocks.StructBlock([('number_of_projects', wagtail.blocks.IntegerBlock(default=3, min_value=1))], group='automatic')), ('spacer', home.blocks.SpacerBlock(group='layout')), ('container', wagtail.blocks.StructBlock([('content', wagtail.blocks.StreamBlock([('CardList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock()))], group='List')), ('HorizontalCardList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock()))], group='List')), ('LinesList', wagtail.blocks.StructBlock([('pages', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['home.HomePage', 'home.Article']))), ('include_images', wagtail.blocks.BooleanBlock(default=True, required=False))], group='List')), ('AboutBlurb', wagtail.blocks.StructBlock([('tagline', wagtail.blocks.CharBlock()), ('column1_text', wagtail.blocks.RichTextBlock()), ('column2_text', wagtail.blocks.RichTextBlock()), ('page', wagtail.blocks.PageChooserBlock())], group='')), ('ContactForm', home.blocks.ContactForm(group='')), ('recent_articles', wagtail.blocks.StructBlock([('number_of_articles', wagtail.blocks.IntegerBlock(default=5, min_value=1))], group='automatic')), ('recent_projects', wagtail.blocks.StructBlock([('number_of_projects', wagtail.blocks.IntegerBlock(default=3, min_value=1))], group='automatic')), ('spacer', home.blocks.SpacerBlock(group='layout')), ('JumbotronCard', wagtail.blocks.StructBlock([('jumbotron', wagtail.blocks.PageChooserBlock())], group='ImageHeader')), ('ImageHeader', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('large', wagtail.blocks.BooleanBlock(default=False, required=False))], group='ImageHeader')), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('text', wagtail.blocks.RichTextBlock(group='basic')), ('image', wagtail.images.blocks.ImageChooserBlock(group='basic', template='blocks/image.html'))]))], group='layout')), ('skipNavMargin', home.blocks.NavMarginBlock(group='layout')), ('JumbotronImageBlock', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('JumbotronCard', wagtail.blocks.StructBlock([('jumbotron', wagtail.blocks.PageChooserBlock())], group='ImageHeader')), ('ImageHeader', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('large', wagtail.blocks.BooleanBlock(default=False, required=False))], group='ImageHeader')), ('ImageDivider', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())], group='ImageHeader')), ('text', wagtail.blocks.RichTextBlock(group='basic')), ('image', wagtail.images.blocks.ImageChooserBlock(group='basic', template='blocks/image.html')), ('table', wagtail.contrib.table_block.blocks.TableBlock(group='basic')), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.blocks.TextBlock(identifier='code', label='Code'))], group='basic', label='Code'))], blank=True, null=True, use_json_field=True),
        ),
    ]
