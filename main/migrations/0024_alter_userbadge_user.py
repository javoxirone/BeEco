# Generated by Django 4.1.7 on 2023-03-25 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0023_remove_badge_category_badge_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbadge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_badge', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]