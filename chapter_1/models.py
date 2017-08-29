from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as __


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True, created_at__lte=timezone.now())

    def unpublished(self):
        return self.filter(
            Q(published=False) |
            Q(created_at__isnull=True) |
            Q(created_at__gt=timezone.now())
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def unpublished(self):
        return self.get_queryset().unpublished()

    def published(self):
        return self.get_queryset().published()

    def publish(self):
        return self.get_queryset().unpublished().update(
            published=True, created_at=timezone.now()
        )


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).published()


class UnpublishedPostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).unpublished()


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=__('Title'))
    slug = models.SlugField(blank=True)
    text = models.TextField(verbose_name=__('Text'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=__('Created at')
    )
    published = models.BooleanField(default=True)

    objects = PostManager()
    without_manager_objects = PostQuerySet.as_manager()
    published_objects = PublishedPostManager()
    unpublished_objects = UnpublishedPostManager()

    def publish(self, commit=True):
        self.published = True
        if commit:
            self.save()
