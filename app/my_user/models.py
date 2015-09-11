# -*- coding: utf-8 -*-
__author__ = 'artem'


from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError(u'Необходимо ввести email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, username=username)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True, verbose_name=u'Логин')
    email = models.EmailField(max_length=255, db_index=True, unique=True, verbose_name=u'Email')
    avatar = models.ImageField(upload_to="user_avatar", default='user_avatar/default.jpg', verbose_name=u'Аватар')
    firstname = models.CharField(max_length=40, null=True, blank=True, verbose_name=u'Фамилия')
    lastname = models.CharField(max_length=40, null=True, blank=True, verbose_name=u'Имя')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=u'Дата рождения')
    register_date = models.DateField(auto_now_add=True, verbose_name=u'Дата регистрации')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'Мобильный телефон')
    is_active = models.BooleanField(default=True, verbose_name=u'Активен')
    is_admin = models.BooleanField(default=False, verbose_name=u'Суперпользователь')

    def get_absolute_url(self):
        return '/private/%d/' % (self.pk)

    # Требуется для админки
    @property
    def is_staff(self):
        return self.is_admin

    def short_firstname(self):
        return "%s." % self.firstname[:1]

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    USERNAME_FIELD = 'username' #Логиниться по username, вместо email
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'