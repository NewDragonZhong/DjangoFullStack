# Generated by Django 2.1.3 on 2018-11-27 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_auto_20181114_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=32, null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('back_info', models.TextField(default='略')),
                ('scope', models.CharField(default='略', max_length=128)),
                ('doc_lis', models.CharField(default='略', max_length=128)),
                ('env_img', models.ImageField(default='略', max_length=128, upload_to='')),
                ('equ_env', models.CharField(max_length=64, null=True)),
                ('hr_lis', models.CharField(max_length=128, null=True)),
                ('func_lis', models.CharField(default='略', max_length=128)),
                ('tac_des', models.CharField(default='略', max_length=128)),
                ('tac_from_con', models.CharField(max_length=128, null=True)),
                ('dev_bug', models.CharField(max_length=128, null=True)),
                ('test_type', models.CharField(default='略', max_length=64)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo')),
            ],
        ),
        migrations.RemoveField(
            model_name='reporttemplate',
            name='user_info',
        ),
        migrations.DeleteModel(
            name='ReportTemplate',
        ),
    ]
