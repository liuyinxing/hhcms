# Generated by Django 2.0.4 on 2018-04-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_auto_20180422_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Comment'),
        ),
    ]
