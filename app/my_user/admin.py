# -*- coding: utf-8 -*-
__author__ = 'artem'


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm
from .forms import UserCreationForm
from .models import MyUser


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        'email',
        'firstname',
        'lastname',
        'username',
        'date_of_birth',
        'phone',
        'is_admin',
        'register_date',

    ]
    list_filter = ('is_admin',)
    fieldsets = (
                (u'Персональные данные', {
                 'fields': (
                     'firstname',
                     'lastname',
                     'username',
                     'email',
                     'date_of_birth',
                     'phone',
                     'avatar',
                 )}),
                (u'Статус суперпользователя да/нет', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'date_of_birth',
                'phone',
                'email',
                'password1',
                'password2',
                'avatar',
            )}
         ),
    )

    search_fields = ('email', 'username',)
    ordering = ('firstname',)
    filter_horizontal = ()

# Регистрация нашей модели
admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)