from django.db import models
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


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
