from django.db import models


class Author(models.Model):
    """ Представляет автора статьи """
    name = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField(null=False, blank=True)


class Category(models.Model):
    """ Представляет категорию статьи """
    name = models.CharField(max_length=40, null=True, blank=True)


class Tag(models.Model):
    """ Представляет тэг, который можно назначить статье """
    name = models.CharField(max_length=20, null=True, blank=True)


class Article(models.Model):
    """ Представляет статью """
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='articles')
