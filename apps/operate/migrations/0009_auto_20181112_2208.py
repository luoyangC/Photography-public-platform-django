# Generated by Django 2.0 on 2018-11-12 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0008_auto_20181108_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='operate.Comment', verbose_name='评论'),
        ),
        migrations.AddField(
            model_name='reply',
            name='source_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='operate.Reply', verbose_name='源回复'),
        ),
        migrations.AlterField(
            model_name='like',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='content.Activity', verbose_name='动态'),
        ),
    ]