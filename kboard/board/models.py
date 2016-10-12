from django.db import models

from django_summernote import models as summer_model
from django_summernote import fields as summer_fields
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

class Board(models.Model):
    def get_absolute_url(self):
        return reverse('board:post_list', args=[self.id])

    name = models.TextField(default='')


class Post(models.Model):
    def get_absolute_url(self):
        return reverse('board:view_post', args=[self.id])

    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)

    class Meta:
        index_together = [
            ["title", "content"],
        ]


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')

class Comment(models.Model):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
