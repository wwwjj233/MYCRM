# Generated by Django 3.0.6 on 2020-06-22 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='permission',
            name='is_menu',
            field=models.BooleanField(default=False),
        ),
    ]
