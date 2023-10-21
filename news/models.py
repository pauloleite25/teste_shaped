from django.db import models
from django.urls import reverse
from django.utils import timezone

from news.managers import LinkManager


class News(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=(
        ('politics', 'Politics'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('technology', 'Technology')
    ))
    created_at = models.DateTimeField(
        db_column='created_at',
        null=True,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        db_column='updated_at',
        null=True,
        auto_now=True
    )

    objects = LinkManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class Link(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    hash_link = models.CharField(max_length=50, unique=True)
    expiration = models.DateTimeField()
    objects = LinkManager()
