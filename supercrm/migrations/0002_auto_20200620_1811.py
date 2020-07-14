# Generated by Django 3.0.6 on 2020-06-20 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supercrm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='appraise',
            field=models.IntegerField(blank=True, choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=32, null=True, verbose_name='评价'),
        ),
        migrations.AlterField(
            model_name='score',
            name='score_date',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='反馈日期'),
        ),
    ]
