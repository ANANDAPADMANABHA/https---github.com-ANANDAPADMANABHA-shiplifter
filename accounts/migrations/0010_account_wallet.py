# Generated by Django 3.2.13 on 2022-07-30 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220715_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='wallet',
            field=models.IntegerField(null=True),
        ),
    ]
