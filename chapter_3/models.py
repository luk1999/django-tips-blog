from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as __


class BasePublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)


class BasePublished(models.Model):
    published = models.BooleanField(default=True)

    objects = BasePublishedQuerySet.as_manager()

    class Meta:
        abstract = True

    def publish(self, commit=True):
        self.published = True
        if commit:
            self.save()


class BaseTracked(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=__('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, verbose_name=__('Updated at')
    )

    class Meta:
        abstract = True


class PostQuerySet(BasePublishedQuerySet):
    def published(self):
        return super().published().filter(created_at__lte=timezone.now())

    def unpublished(self):
        return self.filter(
            Q(published=False) |
            Q(created_at__isnull=True) |
            Q(created_at__gt=timezone.now())
        )


class Post(BasePublished, BaseTracked):
    title = models.CharField(max_length=200, verbose_name=__('Title'))
    slug = models.SlugField(blank=True)
    text = models.TextField(verbose_name=__('Text'))

    objects = PostQuerySet.as_manager()


class HTMLTagger:
    def remove_tags(self, s):
        return strip_tags(s)

    def as_p(self, s):
        return '<p>{}</p>'.format(self.remove_tags(s))

    def as_span(self, s):
        return '<span>{}</span>'.format(self.remove_tags(s))

    def as_div(self, s):
        return '<div>{}</div>'.format(self.remove_tags(s))


class HTMLPost(HTMLTagger, models.Model):
    title = models.CharField(max_length=200, verbose_name=__('Title'))
    slug = models.SlugField(blank=True)
    text = models.TextField(verbose_name=__('Text'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=__('Created at')
    )
    published = models.BooleanField(default=True)

    @property
    def title_as_p(self):
        return self.as_p(self.title)

    @property
    def title_as_span(self):
        return self.as_span(self.title)

    @property
    def title_as_div(self):
        return self.as_div(self.title)


# This model should be created in first application migration, when you're
# using Django >= 1.10.
class User(AbstractUser):
    phone_no = models.CharField(max_length=15, blank=True)


class Customer(User):
    allow_marketing_contact = models.BooleanField(default=True)
