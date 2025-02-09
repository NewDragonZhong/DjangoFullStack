# Generated by Django 2.1.3 on 2019-06-12 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0048_auto_20190612_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='PertestingServersTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_add', models.CharField(max_length=32)),
                ('server_port', models.IntegerField(default=22, max_length=16)),
                ('server_username', models.CharField(max_length=32)),
                ('server_password', models.CharField(max_length=32)),
                ('memory_total', models.IntegerField(default=0, max_length=16)),
                ('memory_used', models.IntegerField(default=0, max_length=16)),
                ('memory_free', models.IntegerField(default=0, max_length=16)),
                ('memory_shard', models.IntegerField(default=0, max_length=16)),
                ('memory_buffCahe', models.IntegerField(default=0, max_length=16)),
                ('memory_available', models.IntegerField(default=0, max_length=16)),
                ('sysLoad_time', models.IntegerField(default=0, max_length=16)),
                ('sysLoad_runTime', models.IntegerField(default=0, max_length=16)),
                ('sysLoad_userNum', models.IntegerField(default=0, max_length=16)),
                ('sysLoad_loadLevel', models.IntegerField(default=0, max_length=16)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo')),
            ],
        ),
    ]
