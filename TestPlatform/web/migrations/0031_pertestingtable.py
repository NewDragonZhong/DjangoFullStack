# Generated by Django 2.1.3 on 2019-05-23 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0030_auto_20190523_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='PertestingTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=32, null=True)),
                ('num', models.CharField(max_length=16, null=True)),
                ('hosts', models.CharField(max_length=32, null=True)),
                ('paths', models.CharField(max_length=64)),
                ('headers', models.CharField(max_length=128)),
                ('datas', models.CharField(max_length=128)),
                ('success_req', models.IntegerField(default=0, max_length=16)),
                ('lose_req', models.IntegerField(default=0, max_length=16)),
                ('count_req', models.IntegerField(default=0, max_length=16)),
                ('avg_time', models.FloatField(default=0.0, max_length=16)),
                ('count_time', models.FloatField(default=0.0, max_length=16)),
                ('loop_num', models.IntegerField(default=0, max_length=16)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo')),
            ],
        ),
    ]
