from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as __


class BasePost(models.Model):
    title = models.CharField(max_length=200, verbose_name=__('Title'))
    slug = models.SlugField(blank=True)
    text = models.TextField(verbose_name=__('Text'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=__('Created at')
    )
    published = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def publish(self, commit=True):
        self.published = True
        if commit:
            self.save()


class News(BasePost):
    pass


class Article(BasePost):
    category = models.CharField(max_length=50)


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True, created_at__lte=timezone.now())


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=__('Title'))
    slug = models.SlugField(blank=True)
    text = models.TextField(verbose_name=__('Text'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=__('Created at')
    )
    published = models.BooleanField(default=True)

    objects = PostQuerySet.as_manager()

    def publish(self, commit=True):
        self.published = True
        if commit:
            self.save()


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).published()


class PublishedPost(Post):
    objects = PublishedPostManager()

    class Meta:
        proxy = True
