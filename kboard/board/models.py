from django.db import models
from ckeditor.fields import RichTextField

class Board(models.Model):
    name = models.TextField(default='')


class Post(models.Model):
    title = models.CharField(default='', max_length=50)
    content = RichTextField()
    board = models.ForeignKey(Board, null=True)

    class Meta:
        unique_together = ('board', 'title')
