# Generated by Django 4.0.7 on 2023-01-28 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_series_tags_alter_article_body_alter_article_header_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='tags',
        ),
    ]
