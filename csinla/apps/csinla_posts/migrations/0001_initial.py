# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-28 08:26
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarInspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engine', models.CharField(blank=True, choices=[('\u6b63\u5e38', '\u6b63\u5e38'), ('\u975e\u6b63\u5e38', '\u975e\u6b63\u5e38')], max_length=15, null=True, verbose_name='\u53d1\u52a8\u673a')),
                ('engine_content', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u53d1\u52a8\u673a\u8be6\u60c5')),
                ('transmission', models.CharField(blank=True, choices=[('\u6b63\u5e38', '\u6b63\u5e38'), ('\u975e\u6b63\u5e38', '\u975e\u6b63\u5e38')], max_length=15, null=True, verbose_name='\u53d8\u901f\u5668')),
                ('transmission_content', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u53d8\u901f\u5668\u8be6\u60c5')),
                ('light', models.CharField(blank=True, choices=[('\u6b63\u5e38', '\u6b63\u5e38'), ('\u975e\u6b63\u5e38', '\u975e\u6b63\u5e38')], max_length=15, null=True, verbose_name='\u524d\u540e\u706f')),
                ('light_content', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u524d\u540e\u706f\u8be6\u60c5')),
                ('colour', models.CharField(choices=[('\u6b63\u5e38', '\u6b63\u5e38'), ('\u975e\u6b63\u5e38', '\u975e\u6b63\u5e38')], max_length=15, null=True, verbose_name='\u539f\u5382\u989c\u8272')),
                ('colour_content', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u539f\u5382\u989c\u8272\u8be6\u60c5')),
                ('circuit', models.CharField(blank=True, choices=[('\u6b63\u5e38', '\u6b63\u5e38'), ('\u975e\u6b63\u5e38', '\u975e\u6b63\u5e38')], max_length=15, null=True, verbose_name='\u7535\u8def')),
                ('circuit_content', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u7535\u8def\u8be6\u60c5')),
                ('tires', models.CharField(blank=True, choices=[('\u6b63\u5e38', '\u6b63\u5e38'), ('\u975e\u6b63\u5e38', '\u975e\u6b63\u5e38')], max_length=15, null=True, verbose_name='\u8f6e\u80ce')),
                ('tires_wear', models.IntegerField(blank=True, null=True, verbose_name='\u8f6e\u80ce\u78e8\u635f\u5ea6')),
                ('tires_content', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u8f6e\u80ce\u8be6\u60c5')),
                ('description', models.CharField(blank=True, choices=[('\u6709', '\u6709'), ('\u65e0', '\u65e0')], max_length=250, null=True, verbose_name='\u6709\u65e0\u6539\u88c5')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u6c7d\u8f66\u6240\u5728\u5730')),
                ('to', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u65e0\u4e8b\u6545\u8f66')),
                ('mileage_min', models.IntegerField(blank=True, null=True, verbose_name='\u91cc\u7a0bmin')),
                ('mileage_max', models.IntegerField(blank=True, null=True, verbose_name='\u91cc\u7a0bmax')),
                ('image', models.ImageField(blank=True, upload_to='carinspection/')),
            ],
            options={
                'verbose_name': '\u6c7d\u8f66\u68c0\u9a8c\u8868\u5355',
                'verbose_name_plural': '\u6c7d\u8f66\u68c0\u9a8c\u8868\u5355',
            },
        ),
        migrations.CreateModel(
            name='MessageImageItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_image', models.ImageField(upload_to='csinla_posts/messageimageitem/content_image/', verbose_name='\u56fe\u7247')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='', max_length=40, verbose_name='\u6807\u9898')),
                ('belong_to', models.CharField(default='\u4e8c\u624b\u8f66', max_length=20, verbose_name='\u5e16\u5b50\u7c7b\u578b')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u53d1\u5e16\u65f6\u95f4')),
                ('expire_date', models.DateTimeField(default=datetime.datetime(2017, 9, 27, 8, 26, 42, 234000, tzinfo=utc), verbose_name='\u5230\u671f\u65f6\u95f4')),
                ('active', models.DateTimeField(default=django.utils.timezone.now)),
                ('reply_num', models.IntegerField(default=0)),
                ('content', models.TextField(blank=True, null=True, verbose_name='\u5185\u5bb9')),
                ('phone', models.CharField(default='0', max_length=15, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('weixin', models.CharField(default='0', max_length=35, verbose_name='\u8054\u7cfb\u5fae\u4fe1')),
                ('is_top', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7f6e\u9876')),
                ('is_notice', models.BooleanField(default=True, verbose_name='\u662f\u5426\u901a\u77e5')),
                ('last_change_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('is_sys', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7cfb\u7edf\u7528\u6237\u53d1\u5e16')),
            ],
            options={
                'ordering': ['post_date'],
                'verbose_name': '\u5e16\u5b50',
                'verbose_name_plural': '\u5e16\u5b50',
            },
        ),
        migrations.CreateModel(
            name='PostHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
                ('remark', models.TextField(verbose_name='\u64cd\u4f5c\u5185\u5bb9')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u64cd\u4f5c\u4eba\u5458')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u5e16\u5b50\u5386\u53f2\u8bb0\u5f55',
                'verbose_name_plural': '\u5e16\u5b50\u5386\u53f2\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='PostMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('level', models.IntegerField(default=0, verbose_name='\u663e\u793a\u4f18\u5148\u7ea7')),
                ('material_status', models.CharField(choices=[('ACTIVE', '\u4f7f\u7528\u4e2d'), ('OVERDUE', '\u5df2\u8fc7\u671f'), ('WAITING', '\u5f85\u5b9a')], default='ACTIVE', max_length=24, verbose_name='\u7d20\u6750\u72b6\u6001')),
                ('material_type', models.CharField(choices=[('EXPOSURE_TOP1', '\u670b\u53cb\u5708\u4e0a\u65b9\uff0890*90\u2014\u2014\u4e34\u65f6\u731c\u6d4b\uff0c\u6839\u636e\u5b9e\u9645\u5b9a\uff09'), ('EXPOSURE_TOP2', '\u670b\u53cb\u5708\u4e0a\u65b9\uff08500*90\u2014\u2014\u4e34\u65f6\u731c\u6d4b\uff0c\u6839\u636e\u5b9e\u9645\u5b9a\uff09')], default='EXPOSURE_TOP1', max_length=24, verbose_name='\u7d20\u6750\u7c7b\u578b')),
                ('content_text', models.CharField(blank=True, max_length=512, null=True, verbose_name='\u6587\u6848')),
                ('content_image', models.ImageField(blank=True, null=True, upload_to='csinla_posts/PostMaterial/content_image/', verbose_name='\u56fe\u7247')),
                ('content_link', models.URLField(blank=True, null=True, verbose_name='\u94fe\u63a5')),
                ('description', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'ordering': ['level', '-create_time'],
                'verbose_name': '\u7d20\u6750',
                'verbose_name_plural': '\u7d20\u6750',
            },
        ),
        migrations.CreateModel(
            name='PostMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4e92\u52a8\u521b\u5efa\u65f6\u95f4')),
                ('content_text', models.TextField(default='', verbose_name='\u5185\u5bb9')),
                ('message_type', models.CharField(choices=[('COLLECT', '\u6536\u85cf'), ('REPLY', '\u56de\u590d')], default='COMMENT', max_length=24, verbose_name='\u4e92\u52a8\u7c7b\u578b')),
                ('floor', models.IntegerField(default=0, verbose_name='\u697c\u5c42')),
                ('is_valid', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6709\u6548')),
                ('has_read', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u67e5\u770b')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u53d1\u8d77\u8005')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u5e16\u5b50\u4e92\u52a8',
                'verbose_name_plural': '\u5e16\u5b50\u4e92\u52a8',
            },
        ),
        migrations.CreateModel(
            name='Rentpicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='house/')),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='house/thumbs/')),
                ('thumbnail_height', models.IntegerField(blank=True, null=True)),
                ('thumbnail_width', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '\u5e16\u5b50\u56fe\u7247',
                'verbose_name_plural': '\u5e16\u5b50\u56fe\u7247',
            },
        ),
        migrations.CreateModel(
            name='UsedBookItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64, verbose_name='\u4e66\u540d')),
                ('price', models.IntegerField(default=0, verbose_name='\u552e\u4ef7')),
                ('isbn', models.CharField(default='', max_length=32, verbose_name='ISBN')),
            ],
        ),
        migrations.CreateModel(
            name='UsedGoodsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64, verbose_name='\u5546\u54c1\u540d')),
                ('price', models.IntegerField(default=0, verbose_name='\u552e\u4ef7')),
            ],
        ),
        migrations.CreateModel(
            name='UsedGoodsTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default='', max_length=128, verbose_name='\u6807\u7b7e\u5185\u5bb9')),
            ],
            options={
                'verbose_name': '\u4e8c\u624b\u6807\u7b7e',
                'verbose_name_plural': '\u4e8c\u624b\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='ViewRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(verbose_name='\u8bb0\u5f55\u65e5\u671f')),
                ('belong_to', models.CharField(max_length=20, verbose_name='\u5e16\u5b50\u7c7b\u578b')),
                ('view_count', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
                ('user_count', models.IntegerField(default=0, verbose_name='\u6d4f\u89c8\u7528\u6237\u6570')),
                ('collect_count', models.IntegerField(default=0, verbose_name='\u6536\u85cf\u7528\u6237\u6570')),
                ('last_change_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('join_list', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='\u8bbf\u95ee\u7528\u6237')),
            ],
            options={
                'ordering': ['-create_date'],
                'verbose_name': '\u6a21\u5757\u6d4f\u89c8\u8bb0\u5f55',
                'verbose_name_plural': '\u6a21\u5757\u6d4f\u89c8\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('car_id', models.CharField(default='C1127', max_length=20)),
                ('car_type', models.CharField(default='Japanese', max_length=10)),
                ('car_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('brand', models.TextField(max_length=20)),
                ('vehicle_age', models.CharField(default=0, max_length=20, verbose_name='\u8f66\u9f84')),
                ('vehicle_miles', models.CharField(default=0, max_length=20, verbose_name='\u884c\u9a76\u91cc\u7a0b')),
                ('fee', models.CharField(default=0, max_length=10, verbose_name='\u4ef7\u683c')),
                ('fee2', models.IntegerField(default=0, verbose_name='\u4ef7\u683c2')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12, verbose_name='\u4ef7\u683c\uff08\u5206\u6570\uff09')),
                ('price2', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12, verbose_name='\u4ef7\u683c\uff08\u5206\u65702\uff09')),
                ('level_type', models.CharField(default='other', max_length=10)),
                ('level_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('transmission_type', models.CharField(choices=[('\u81ea\u52a8', '\u81ea\u52a8'), ('\u624b\u52a8', '\u624b\u52a8')], default='auto', max_length=10)),
                ('displacement', models.CharField(default=0, max_length=30)),
                ('drive_type', models.CharField(choices=[('\u524d\u9a71', '\u524d\u9a71'), ('\u540e\u9a71', '\u540e\u9a71'), ('\u56db\u9a71', '\u56db\u9a71')], max_length=20, null=True)),
                ('inside_color', models.TextField(max_length=50, null=True)),
                ('outside_color', models.TextField(max_length=50, null=True)),
                ('oil_type', models.CharField(choices=[('\u6c7d\u6cb9', '\u6c7d\u6cb9'), ('\u67f4\u6cb9', '\u67f4\u6cb9'), ('\u6cb9\u7535\u6df7\u5408', '\u6cb9\u7535\u6df7\u5408'), ('\u7535\u529b', '\u7535\u529b')], max_length=10, null=True)),
                ('turbo', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], max_length=10, null=True)),
                ('vin_number', models.CharField(max_length=20)),
                ('contactor', models.TextField(default='admin', max_length=100)),
                ('contact_way', models.TextField(default='', max_length=100)),
            ],
            options={
                'ordering': ['-post_date'],
                'verbose_name': '\u6c7d\u8f66',
                'verbose_name_plural': '\u6c7d\u8f66',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='EntireRent',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('house_id', models.CharField(default='H1', max_length=20)),
                ('rent_begins', models.DateField(default=django.utils.timezone.now)),
                ('rent_ends', models.DateField(default=django.utils.timezone.now)),
                ('district', models.CharField(max_length=20, null=True)),
                ('district_other', models.CharField(blank=True, max_length=10, null=True)),
                ('fee', models.IntegerField(default=0)),
                ('share', models.CharField(choices=[('private', 'private'), ('share', 'share')], max_length=10, null=True)),
                ('house_type', models.CharField(default='other', max_length=10)),
                ('house_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('room_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('pet', models.CharField(choices=[('\u5141\u8bb8', '\u5141\u8bb8'), ('\u4e0d\u5141\u8bb8', '\u4e0d\u5141\u8bb8')], max_length=10, null=True)),
                ('smoke', models.CharField(choices=[('\u5141\u8bb8', '\u5141\u8bb8'), ('\u4e0d\u5141\u8bb8', '\u4e0d\u5141\u8bb8')], max_length=10, null=True)),
                ('parking', models.CharField(choices=[('\u6709', '\u6709'), ('\u65e0', '\u65e0'), ('street parking', 'street parking')], max_length=20, null=True)),
                ('pak_nums', models.CharField(max_length=10, null=True, verbose_name='\u505c\u8f66\u4f4d\u4e2a\u6570')),
                ('driving_time_toschool_hour', models.CharField(default='0', max_length=20)),
                ('driving_time_toschool_minute', models.CharField(default='0', max_length=20)),
                ('transit_time_toschool_hour', models.CharField(default='0', max_length=20)),
                ('transit_time_toschool_minute', models.CharField(default='0', max_length=20)),
                ('address', models.TextField(max_length=100)),
                ('contactor', models.TextField(default='admin', max_length=30)),
                ('contact_way', models.TextField(default='87654321', max_length=50)),
            ],
            options={
                'ordering': ['-post_date'],
                'verbose_name': '\u6574\u5957\u51fa\u79df',
                'verbose_name_plural': '\u6574\u5957\u51fa\u79df',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('temp', models.CharField(default='', max_length=32, verbose_name='\u65e0\u6548\u5b57\u6bb5')),
            ],
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('house_id', models.CharField(default='H1', max_length=20)),
                ('rent_begins', models.DateField(default=django.utils.timezone.now)),
                ('rent_ends', models.DateField(default=django.utils.timezone.now)),
                ('district', models.CharField(max_length=20, null=True)),
                ('district_other', models.CharField(blank=True, max_length=10, null=True)),
                ('fee', models.IntegerField(default=0)),
                ('share', models.CharField(choices=[('private', 'private'), ('share', 'share')], max_length=10, null=True)),
                ('house_type', models.CharField(default='other', max_length=10)),
                ('house_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('room_type', models.CharField(default='other', max_length=10)),
                ('room_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('pet', models.CharField(choices=[('\u5141\u8bb8', '\u5141\u8bb8'), ('\u4e0d\u5141\u8bb8', '\u4e0d\u5141\u8bb8')], max_length=10, null=True)),
                ('smoke', models.CharField(choices=[('\u5141\u8bb8', '\u5141\u8bb8'), ('\u4e0d\u5141\u8bb8', '\u4e0d\u5141\u8bb8')], max_length=10, null=True)),
                ('parking', models.CharField(choices=[('\u6709', '\u6709'), ('\u65e0', '\u65e0'), ('street parking', 'street parking')], max_length=20, null=True)),
                ('gender_require', models.CharField(choices=[('\u9650\u7537\u751f', '\u9650\u7537\u751f'), ('\u9650\u5973\u751f', '\u9650\u5973\u751f'), ('\u4e0d\u9650\u5236', '\u4e0d\u9650\u5236')], default='no_requirement', max_length=20)),
                ('driving_time_toschool_hour', models.CharField(default='0', max_length=20)),
                ('driving_time_toschool_minute', models.CharField(default='0', max_length=20)),
                ('transit_time_toschool_hour', models.CharField(default='0', max_length=20)),
                ('transit_time_toschool_minute', models.CharField(default='0', max_length=20)),
                ('address', models.TextField(max_length=100)),
                ('contactor', models.TextField(default='admin', max_length=30)),
                ('contact_way', models.TextField(default='87654321', max_length=50)),
            ],
            options={
                'ordering': ['-post_date'],
                'verbose_name': '\u4e2a\u4eba\u8f6c\u79df',
                'verbose_name_plural': '\u4e2a\u4eba\u8f6c\u79df',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='Rent2',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('house_id', models.CharField(default='H1127', max_length=20)),
                ('rent_begins', models.DateField(default=django.utils.timezone.now)),
                ('rent_ends', models.DateField(default=django.utils.timezone.now)),
                ('district', models.CharField(blank=True, max_length=10, null=True)),
                ('district_other', models.CharField(blank=True, max_length=10, null=True)),
                ('fee', models.IntegerField(default=0)),
                ('occupy_limit', models.IntegerField(default=1)),
                ('house_type', models.CharField(default='other', max_length=10)),
                ('house_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('room_type', models.CharField(default='other', max_length=10)),
                ('room_type_other', models.CharField(blank=True, max_length=10, null=True)),
                ('pet', models.CharField(blank=True, choices=[('\u5141\u8bb8', '\u5141\u8bb8'), ('\u4e0d\u5141\u8bb8', '\u4e0d\u5141\u8bb8')], max_length=10, null=True)),
                ('smoke', models.CharField(blank=True, choices=[('\u5141\u8bb8', '\u5141\u8bb8'), ('\u4e0d\u5141\u8bb8', '\u4e0d\u5141\u8bb8')], max_length=10, null=True)),
                ('parking', models.CharField(blank=True, choices=[('\u6709', '\u6709'), ('\u65e0', '\u65e0'), ('street parking', 'street parking')], max_length=20, null=True)),
                ('gender_require', models.CharField(choices=[('male_only', 'male_only'), ('female_only', 'female_only'), ('no_requirement', 'no_requirement')], default='no_requirement', max_length=20)),
                ('driving_time_toschool', models.IntegerField(default=0)),
                ('transit_time_toschool', models.IntegerField(default=0)),
                ('address', models.TextField(max_length=100)),
                ('contactor', models.TextField(default='admin', max_length=30)),
                ('contact_way', models.TextField(default='87654321', max_length=50)),
            ],
            options={
                'verbose_name': '\u5408\u79df',
                'verbose_name_plural': '\u5408\u79df',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='Used',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('used_id', models.CharField(default='', max_length=32, verbose_name='\u4e8c\u624b\u7f16\u53f7')),
                ('district', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='\u5730\u533a')),
                ('address', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='\u5177\u4f53\u5730\u5740')),
                ('connect_name', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u4eba')),
                ('connect_phone', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('connect_wx', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u5fae\u4fe1')),
                ('content_detail', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='\u8be6\u7ec6\u5185\u5bb9')),
                ('tags', models.ManyToManyField(blank=True, default='', null=True, to='csinla_posts.UsedGoodsTag', verbose_name='\u6807\u7b7e')),
            ],
            options={
                'ordering': ['-post_date'],
                'verbose_name': '\u4e8c\u624b',
                'verbose_name_plural': '\u4e8c\u624b',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='UsedBook',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('book_id', models.CharField(default='', max_length=32, verbose_name='\u4e66\u53f7')),
                ('district', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u5730\u533a')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u5177\u4f53\u5730\u5740')),
                ('connect_name', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u4eba')),
                ('connect_phone', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('connect_wx', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u5fae\u4fe1')),
                ('content_detail', DjangoUeditor.models.UEditorField(blank=True, verbose_name='\u8be6\u7ec6\u5185\u5bb9')),
            ],
            options={
                'ordering': ['-post_date'],
                'verbose_name': '\u4e8c\u624b\u4e66',
                'verbose_name_plural': '\u4e8c\u624b\u4e66',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.CreateModel(
            name='UsedGoods',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='csinla_posts.Post')),
                ('used_id', models.CharField(default='', max_length=32, verbose_name='\u5546\u54c1\u53f7')),
                ('district', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u5730\u533a')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u5177\u4f53\u5730\u5740')),
                ('connect_name', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u4eba')),
                ('connect_phone', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('connect_wx', models.CharField(default='', max_length=100, verbose_name='\u8054\u7cfb\u5fae\u4fe1')),
                ('content_detail', DjangoUeditor.models.UEditorField(blank=True, verbose_name='\u8be6\u7ec6\u5185\u5bb9')),
                ('tags', models.ManyToManyField(blank=True, null=True, to='csinla_posts.UsedGoodsTag', verbose_name='\u6807\u7b7e')),
            ],
            options={
                'ordering': ['-post_date'],
                'verbose_name': '\u4e8c\u624b\u5546\u54c1',
                'verbose_name_plural': '\u4e8c\u624b\u5546\u54c1',
            },
            bases=('csinla_posts.post',),
        ),
        migrations.AddField(
            model_name='rentpicture',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.Post'),
        ),
        migrations.AddField(
            model_name='postmessage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.Post', verbose_name='\u5bf9\u5e94\u5e16\u5b50'),
        ),
        migrations.AddField(
            model_name='postmessage',
            name='reply_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.PostMessage', verbose_name='\u56de\u590d\u7684\u7559\u8a00'),
        ),
        migrations.AddField(
            model_name='posthistory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.Post', verbose_name='\u5bf9\u5e94\u5e16\u5b50'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005'),
        ),
        migrations.AddField(
            model_name='messageimageitem',
            name='postmessage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.PostMessage', verbose_name='\u5bf9\u5e94\u6d88\u606f'),
        ),
        migrations.AddField(
            model_name='usedgoodsitem',
            name='usedgoods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.UsedGoods'),
        ),
        migrations.AddField(
            model_name='usedbookitem',
            name='usedbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csinla_posts.UsedBook'),
        ),
        migrations.AddField(
            model_name='carinspection',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car', to='csinla_posts.Car'),
        ),
    ]