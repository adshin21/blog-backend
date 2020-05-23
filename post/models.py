from django.db import models
from users.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from secrets import token_hex


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    delta = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    draft = models.BooleanField(default=False)
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add=True)


def unique_slug_generator(instance, new_slug=None, **kwargs):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title) + '_' + token_hex(20)

    qs_exists = Blog.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}_{randstr}".format(
            slug=slug.split('_'),
            randstr=token_hex(20)
        )
        return unique_slug_generator(
            instance,
            new_slug=new_slug,
        )
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_post_receiver, sender=Blog)
