# Generated by Django 4.2.7 on 2023-11-21 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclub',
            name='discussion',
            field=models.TextField(blank=True, null=True),
        ),
    ]