# -*- coding: utf-8 -*-
__author__ = 'artem'

from django.db import models
from app.settings import AUTH_USER_MODEL

class User_CV(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, related_name="user_cv")
    cv = models.FileField(upload_to="cv_files")

    def __unicode__(self):
        return u"Резюме %s" % self.pk

    class Meta:
        verbose_name = u'Резюме'
        verbose_name_plural = u'Резюме'
