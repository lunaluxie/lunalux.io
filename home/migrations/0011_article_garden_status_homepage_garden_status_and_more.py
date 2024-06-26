# Generated by Django 4.2 on 2024-06-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='garden_status',
            field=models.CharField(choices=[('na', 'None'), ('seedling', '🌱 Seedling: For rough and early ideas'), ('budding', '🌿 Budding: For work that has been cleaned up and clarified'), ('evergreen', "🌳 Evergreen: For work that's reasonably complete, but might still receive updates.")], default='na', max_length=10),
        ),
        migrations.AddField(
            model_name='homepage',
            name='garden_status',
            field=models.CharField(choices=[('na', 'None'), ('seedling', '🌱 Seedling: For rough and early ideas'), ('budding', '🌿 Budding: For work that has been cleaned up and clarified'), ('evergreen', "🌳 Evergreen: For work that's reasonably complete, but might still receive updates.")], default='na', max_length=10),
        ),
        migrations.AddField(
            model_name='series',
            name='garden_status',
            field=models.CharField(choices=[('na', 'None'), ('seedling', '🌱 Seedling: For rough and early ideas'), ('budding', '🌿 Budding: For work that has been cleaned up and clarified'), ('evergreen', "🌳 Evergreen: For work that's reasonably complete, but might still receive updates.")], default='na', max_length=10),
        ),
    ]