# Generated by Django 2.1.3 on 2019-06-11 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0045_pertestingtable'),
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
                ('procss_r', models.IntegerField(max_length=16)),
                ('procss_b', models.IntegerField(max_length=16)),
                ('memory_free', models.IntegerField(max_length=16)),
                ('memory_buff', models.IntegerField(max_length=16)),
                ('memory_cache', models.IntegerField(max_length=16)),
                ('cpu_us', models.IntegerField(max_length=16)),
                ('cpu_sy', models.IntegerField(max_length=16)),
                ('cpu_id', models.IntegerField(max_length=16)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo')),
            ],
        ),
    ]
