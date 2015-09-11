# -*- coding: utf-8 -*-
__author__ = 'artem'

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from my_user.models import MyUser
from app.forms import RegistrationForm, PrivateEditForm, UserAddCVForm, UserEditCVForm, ContactForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cv.models import User_CV
from app import settings


class HomeView(ListView):
    model = MyUser
    context_object_name = 'cv'
    template_name = "home.html"


class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    model = MyUser
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        subject = "Создан новый аккаунт"
        to = [self.object.email]
        from_email = u"test_cv <art.ef.1991@gmail.com>"

        ctx = {
            "firstname": self.object.firstname,
            "lastname": self.object.lastname,
            "username": self.object.username,
            "email": self.object.email,
            "date_of_birth": self.object.date_of_birth,
            "phone": self.object.phone,
            "registered": self.object.register_date,
            "password": form.cleaned_data['password2']
        }

        message = render_to_string('registration/email.txt', ctx)
        msg = EmailMessage(subject, message, from_email=from_email, to=to)
        msg.send()
        return super(RegistrationView, self).form_valid(form)


class PrivateView(DetailView):
    model = MyUser
    template_name = 'private_detail.html'
    context_object_name = 'is_private'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PrivateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrivateView, self).get_context_data(**kwargs)
        context['is_private'] = True
        return context


class PrivateEditView(UpdateView):
    template_name = 'edit_user.html'
    model = MyUser
    form_class = PrivateEditForm

    def get_context_data(self, **kwargs):
        context = super(PrivateEditView, self).get_context_data(**kwargs)
        context['is_private'] = True
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(PrivateEditView, self).form_valid(form)


class PrivateDeleteView(DeleteView):
    model = MyUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(PrivateDeleteView, self).get_context_data(**kwargs)
        context['is_private'] = True
        return context


class DetailCVView(TemplateView):
    template_name = 'detail_cv.html'

    def get_context_data(self, **kwargs):
        context = super(DetailCVView, self).get_context_data(**kwargs)
        context['is_home'] = True
        return context


class AddCVView(CreateView):
    template_name = 'add_cv.html'
    model = User_CV
    form_class = UserAddCVForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(AddCVView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddCVView, self).get_context_data(**kwargs)
        context['is_home'] = True
        return context

    def get_success_url(self):
        user_id = self.object.pk
        return reverse('user_cv', args=(self.request.user.pk,))


class EditCVView(UpdateView):
    template_name = 'add_cv.html'
    model = User_CV
    form_class = UserEditCVForm

    def get_object(self, queryset=None):
        return User_CV.objects.get(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EditCVView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditCVView, self).get_context_data(**kwargs)
        context['is_home'] = True
        return context

    def get_success_url(self):
        return reverse('user_cv', args=(self.request.user.pk,))


class DeleteCVView(DeleteView):
    model = User_CV
    template_name = 'delete_cv.html'

    def get_object(self, queryset=None):
        return User_CV.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DeleteCVView, self).get_context_data(**kwargs)
        context['is_home'] = True
        return context

    def get_success_url(self):
        return reverse('user_cv', args=(self.request.user.pk,))


class ContactsView(FormView):
    form_class = ContactForm
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        context['is_contacts'] = True
        return context

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        to = settings.EMAIL_HOST_USER
        from_email = "%s <%s>" % (form.cleaned_data['name'], form.cleaned_data['email'])

        ctx = {
            "name": form.cleaned_data['name'],
            "email": form.cleaned_data['email'],
            "message": form.cleaned_data['message']
        }

        message = render_to_string('email.txt', ctx)
        msg = EmailMessage(subject, message, from_email=from_email, to=[to])
        msg.send()
        return super(ContactsView, self).form_valid(form)

    def get_success_url(self):
        return '/survey_answer/'