# Generated by Django 4.1.7 on 2023-03-25 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_userbadge_badge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileimage',
            name='image',
            field=models.ImageField(blank=True, default='https://экологиякрыма.рф/img/19893719.jpg', null=True, upload_to='profile/', verbose_name='Рисунок'),
        ),
    ]