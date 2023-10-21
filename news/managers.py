from django.utils import timezone
from django.db import models
from news.helpers import generate_link_hask


class LinkManager(models.Manager):

    def create_link(self, news):
        hash_link = generate_link_hask()
        expiration = timezone.now() + timezone.timedelta(hours=1)
        return self.update_or_create(news=news, hash_link=hash_link, expiration=expiration)