from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator


class Tag(models.Model):
    caption = models.CharField(max_length=16)

    def __str__(self):
        return self.caption

    # class Meta:
    #     verbose_name_plural = 'Tags'


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Post(models.Model):
    title = models.CharField(max_length=64)
    excerpt = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images', null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=32)
    user_email = models.EmailField(max_length=64)
    text = models.TextField(max_length=512)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')