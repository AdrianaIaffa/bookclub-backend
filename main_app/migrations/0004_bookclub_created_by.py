# Generated by Django 4.2.7 on 2023-11-21 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_alter_bookclub_members_alter_comment_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclub',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_bookclubs', to=settings.AUTH_USER_MODEL),
        ),
    ]
