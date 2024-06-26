# Generated by Django 4.2 on 2024-06-26 17:03

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('home', '0013_alter_pagetag_content_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.PageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='series',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='home.PageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
