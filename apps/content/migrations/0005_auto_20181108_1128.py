# Generated by Django 2.0 on 2018-11-08 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20181107_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='comment_nums',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='keep_nums',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='like_nums',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='share_nums',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='comment_nums',
        ),
    ]
