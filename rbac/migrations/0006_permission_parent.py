# Generated by Django 3.0.6 on 2020-06-27 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_menu_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission'),
        ),
    ]
