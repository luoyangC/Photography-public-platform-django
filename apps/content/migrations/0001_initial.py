# Generated by Django 2.0.8 on 2019-02-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='状态')),
                ('content', models.TextField(verbose_name='内容')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('activity_type', models.CharField(choices=[('original', '原创'), ('forward', '转载')], max_length=10, verbose_name='动态类型')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='地址')),
            ],
            options={
                'verbose_name': '动态',
                'verbose_name_plural': '动态',
            },
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='状态')),
                ('content', models.TextField(verbose_name='内容')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('agreement_type', models.CharField(choices=[('free', '互免'), ('toll', '收费'), ('paid', '付费')], max_length=5, verbose_name='约拍类型')),
                ('amount', models.FloatField(default=0, verbose_name='金额')),
                ('tags', models.CharField(blank=True, max_length=100, null=True, verbose_name='标签')),
                ('address', models.CharField(max_length=100, verbose_name='地址')),
            ],
            options={
                'verbose_name': '约拍',
                'verbose_name_plural': '约拍',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='状态')),
                ('image', models.ImageField(upload_to='image/content/%Y/%m', verbose_name='图片')),
            ],
            options={
                'verbose_name': '照片',
                'verbose_name_plural': '照片',
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='状态')),
                ('image', models.ImageField(upload_to='image/content/%Y/%m', verbose_name='样张')),
            ],
            options={
                'verbose_name': '样张',
                'verbose_name_plural': '样张',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='状态')),
                ('title', models.CharField(max_length=50, verbose_name='主题名称')),
                ('info', models.CharField(max_length=500, verbose_name='主题描述')),
                ('follow_nums', models.IntegerField(default=0, verbose_name='关注数')),
                ('image', models.ImageField(default='/image/topic/default.png', upload_to='image/topic/%Y/%m', verbose_name='图片')),
            ],
            options={
                'verbose_name': '主题',
                'verbose_name_plural': '主题',
            },
        ),
    ]
