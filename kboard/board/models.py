from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

from django_summernote import fields as summer_fields
from django_summernote import models as summer_model

from core.models import TimeStampedModel


class Board(models.Model):
    def get_absolute_url(self):
        return reverse('board:post_list', args=[self.slug])

    slug = models.TextField(default='', unique=True)
    name = models.TextField(default='')


class PostQuerySet(models.QuerySet):
    def search(self, search_flag, query):
        if search_flag == 'TITLE':
            return self.filter(title__contains=query)
        elif search_flag == 'CONTENT':
            return self.filter(content__contains=query)
        elif search_flag == 'BOTH':
            return self.filter(Q(title__contains=query) | Q(content__contains=query))
        else:
            return self.all()

    def remain(self):
        return self.filter(is_deleted=False)

    def get_from_board(self, board):
        return self.filter(board=board)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, search_flag, query):
        return self.get_queryset().search(search_flag, query)

    def remain(self):
        return self.get_queryset().remain()

    def get_from_board(self, board):
        return self.get_queryset().get_from_board(board)


class Post(TimeStampedModel):
    def get_absolute_url(self):
        return reverse('board:view_post', args=[self.id])

    objects = PostManager()

    title = models.TextField(default='')
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True)
    is_deleted = models.BooleanField(default=False)
    page_view_count = models.IntegerField(default=0)


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class Comment(TimeStampedModel):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True)
    is_deleted = models.BooleanField(default=False)


class EditedPostHistory(TimeStampedModel):
    post = models.ForeignKey(Post, null=False, default=None)
    title = models.TextField(default='')
    content = models.TextField(default='')

class Registration(AbstractUser):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    username = models.CharField(max_length=30, unique=True, default='')
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=75)
    joined = models.DateTimeField(auto_now_add=True)
