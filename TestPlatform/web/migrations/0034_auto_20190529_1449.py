# Generated by Django 2.1.3 on 2019-05-29 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0033_pertestingtable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pertestingtable',
            name='user_info',
        ),
        migrations.DeleteModel(
            name='PertestingTable',
        ),
    ]
