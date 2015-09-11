# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User_CV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cv', models.FileField(upload_to=b'cv_files')),
                ('user', models.OneToOneField(related_name='user_cv', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0437\u044e\u043c\u0435',
                'verbose_name_plural': '\u0420\u0435\u0437\u044e\u043c\u0435',
            },
        ),
    ]
