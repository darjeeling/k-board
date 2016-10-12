from django.db import models
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields
from django.core.paginator import Paginator

class Board(models.Model):
    name = models.TextField(default='')


class Post(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)

    class Meta:
        unique_together = ('board', 'title')


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')

class Comment(models.Model):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
