# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(verbose_name='message')),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added')),
                ('unseen', models.BooleanField(default=True, verbose_name='unseen')),
                ('archived', models.BooleanField(default=False, verbose_name='archived')),
                ('on_site', models.BooleanField(default=False, verbose_name='on site')),
            ],
            options={
                'ordering': ['-added'],
                'verbose_name': 'notice',
                'verbose_name_plural': 'notices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeQueueBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pickled_data', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('medium', models.CharField(max_length=1, verbose_name='medium', choices=[(b'1', 'Email')])),
                ('send', models.BooleanField(default=False, verbose_name='send')),
            ],
            options={
                'verbose_name': 'notice setting',
                'verbose_name_plural': 'notice settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=40, verbose_name='label')),
                ('display', models.CharField(max_length=50, verbose_name='display')),
                ('description', models.CharField(max_length=100, verbose_name='description')),
                ('default', models.IntegerField(verbose_name='default')),
            ],
            options={
                'verbose_name': 'notice type',
                'verbose_name_plural': 'notice types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ObservedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added')),
                ('signal', models.TextField(verbose_name='signal')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('notice_type', models.ForeignKey(verbose_name='notice type', to='notification.NoticeType')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-added'],
                'verbose_name': 'observed item',
                'verbose_name_plural': 'observed items',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='noticesetting',
            name='notice_type',
            field=models.ForeignKey(verbose_name='notice type', to='notification.NoticeType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noticesetting',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='noticesetting',
            unique_together=set([('user', 'notice_type', 'medium')]),
        ),
        migrations.AddField(
            model_name='notice',
            name='notice_type',
            field=models.ForeignKey(verbose_name='notice type', to='notification.NoticeType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notice',
            name='recipient',
            field=models.ForeignKey(related_name='recieved_notices', verbose_name='recipient', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notice',
            name='sender',
            field=models.ForeignKey(related_name='sent_notices', verbose_name='sender', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.RunSQL(
            sql="""CREATE INDEX notification_notice_recipient_on_site_unseen
    ON notification_notice
    USING btree
    (recipient_id, on_site, unseen)
    WHERE on_site = true AND unseen = true;""",
        ),
    ]
