# Generated by Django 2.1.3 on 2019-05-29 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0035_pertestingtable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pertestingtable',
            name='maxnum',
            field=models.IntegerField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='pertestingtable',
            name='oncenum',
            field=models.IntegerField(max_length=16, null=True),
        ),
    ]
