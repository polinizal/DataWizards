# Generated by Django 5.1.7 on 2025-03-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('madS', '0009_merge_0007_article_title_0008_alter_survey_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
