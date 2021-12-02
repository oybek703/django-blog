from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=32)


class Post(models.Model):
    title = models.CharField(max_length=64)
    excerpt = models.CharField(max_length=128)
    image_name = models.CharField(max_length=128)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(default='', null=False, blank=True, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tags(models.Model):
    caption = models.CharField(max_length=16)
    author = models.ManyToManyField(Author)
    post = models.ManyToManyField(Post)

    class Meta:
        verbose_name_plural = 'Tags'
