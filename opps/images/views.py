# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator

from .forms import PopUpImageForm
from .models import Image


class PopUpImageView(FormView):
    form_class = PopUpImageForm
    template_name = 'images/image_add.html'

    def get_form_kwargs(self):
        kwargs = super(PopUpImageView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        return render(self.request, 'images/popup_done.html',
                      {'image': instance})


class GetImagesView(ListView):
    model = Image
    context_object_name = 'images'

    def get_template_names(self):
        if self.request.GET.get('template_name'):
            return ['images/{0}'.format(self.request.GET.get('template_name'))]
        return ['images/all_images.html']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GetImagesView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(GetImagesView, self).get_queryset().order_by('-id')

        query = Q()
        q = self.request.GET.get("q")
        user = self.request.GET.get("user") or 0
        published = self.request.GET.get("published", 1)

        if q:
            query &= Q(title__icontains=q) | Q(description__icontains=q)

        if user:
            query &= Q(user__id=user)

        if published:
            query &= Q(published=int(published))

        queryset = queryset.filter(query)
        return queryset._clone()

    def get_context_data(self, *args, **kwargs):
        q = self.request.GET.get("q")
        user = self.request.GET.get("user") or 0
        published = self.request.GET.get("published")

        context = {
            'users': get_user_model().objects.filter(
                image__isnull=False
            ).order_by('email').values('id', 'email').distinct(),
            'user_id': int(user),
            'published': published,
            'q': q,
        }
        context.update(kwargs)
        return super(GetImagesView, self).get_context_data(**context)
