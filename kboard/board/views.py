from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.db.models import F
from django.db import transaction

from registration.backends.hmac.views import RegistrationView
from registration.backends.hmac.views import ActivationView

from board.models import Post, Board, Comment
from board.forms import PostForm, CustomizeRegistrationForm
from core.utils import get_pages_nav_info


def new_post(request, board_slug):
    if request.method == 'POST':
        board = Board.objects.get(slug=board_slug)
        Post.objects.create(board=board, title=request.POST['post_title_text'], content=request.POST['fields'])
        return redirect(reverse('board:post_list', args=[board_slug]))

    board = Board.objects.get(slug=board_slug)
    form = PostForm()
    return render(request, 'new_post.html', {'board': board, 'form': form})


def post_list(request, board_slug):
    board = Board.objects.get(slug=board_slug)
    # search
    query = request.GET.get('query', '')
    if query:
        posts = Post.objects.get_from_board(board).remain().search(query).order_by('-id')
    else:
        posts = Post.objects.get_from_board(board).remain().order_by('-id')

    # pagination
    paginator = Paginator(posts, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(posts, nav_chunk_size=10)

    return render(request, 'post_list.html', {
        'posts': posts,
        'board_slug': board_slug,
        'pages_nav_info': pages_nav_info,
        'query': query
    })


def view_post(request, post_id):
    non_sliced_query_set = Post.objects.filter(id=post_id)
    non_sliced_query_set.update(page_view_count=F('page_view_count') + 1)

    post = Post.objects.get(id=post_id)
    comments_all_list = Comment.objects.filter(post=post, is_deleted=False).order_by('-id')

    paginator = Paginator(comments_all_list, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(comments, nav_chunk_size=10)

    return render(request, 'view_post.html', {
        'post': post,
        'comments': comments,
        'pages_nav_info': pages_nav_info
    })


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post.title = request.POST['post_title_text']
        post.content = request.POST.get('fields', '')
        post.save()
        return redirect(post.board)

    form = PostForm(initial={'fields': post.content})
    return render(request, 'edit_post.html', {'post': post, 'form': form})


def board_list(request):
    board_count = Board.objects.all().count()
    if board_count == 0:
        Board.objects.create(name='Default', slug='default')

    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})


@require_POST
def new_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, content=request.POST['comment_content'])
        return redirect(post)


@require_POST
def delete_comment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.is_deleted = True
        comment.save()

        return redirect(comment.post)


@require_POST
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.is_deleted = True
        post.save(update_fields=['is_deleted'])

        return redirect(post.board)


class CustomizeRegistrationView(RegistrationView):

    form_class = CustomizeRegistrationForm

    @transaction.atomic
    def create_inactive_user(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def get_activation_key(self, user):
        pass

    def get_email_context(self, activation_key):
        pass

    def send_activation_email(self, user):
        pass


class CustomizeActivationView(ActivationView):
    def get_user(self, username):
        pass

    def validate_key(self, activation_key):
        pass
