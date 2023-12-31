# Generated by Django 4.2.7 on 2023-11-21 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0006_alter_bookclub_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookclub',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_bookclubs', to=settings.AUTH_USER_MODEL),
        ),
    ]
