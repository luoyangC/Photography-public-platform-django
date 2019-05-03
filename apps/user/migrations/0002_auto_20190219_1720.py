# Generated by Django 2.0.8 on 2019-02-19 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_url',
            field=models.URLField(blank=True, null=True, verbose_name='微信头像'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/user/default.png', upload_to='image/user/%Y/%m', verbose_name='自定义头像'),
        ),
    ]