import re

from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import (
    ugettext,
    ugettext_lazy,
)


class Post(models.Model):
    name = models.CharField(max_length=50, verbose_name=ugettext_lazy('Name'))
    slug = models.CharField(max_length=50, verbose_name=ugettext_lazy('Slug'))

    class Meta:
        verbose_name = ugettext_lazy('Post')
        verbose_name_plural = ugettext_lazy('Posts')

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if not re.match(r'^[A-Za-z0-9\-]*$', slug):
            raise ValidationError({
                'slug': ugettext('Only letters, digits and - is allowed.')
            })
        return slug
