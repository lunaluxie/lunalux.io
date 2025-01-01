# Generated by Django 5.1 on 2025-01-01 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_article_article_type_alter_article_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='starred',
            field=models.BooleanField(default=False, help_text='If starred, a star will be displayed next to the page in the list of articles'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='starred',
            field=models.BooleanField(default=False, help_text='If starred, a star will be displayed next to the page in the list of articles'),
        ),
        migrations.AddField(
            model_name='series',
            name='starred',
            field=models.BooleanField(default=False, help_text='If starred, a star will be displayed next to the page in the list of articles'),
        ),
    ]
