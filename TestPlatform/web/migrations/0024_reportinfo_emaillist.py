# Generated by Django 2.1.3 on 2018-12-05 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0023_remove_modalinfo_func_lis'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportinfo',
            name='emailList',
            field=models.CharField(default='略', max_length=128),
        ),
    ]
