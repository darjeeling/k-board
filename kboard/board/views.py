from django.shortcuts import render, redirect

from board.models import Post, Board
from board.forms import PostForm


def new_post(request):
    board = Board.objects.get(id=request.GET['board'])
    form = PostForm()
    return render(request, 'new_post.html', {'board': board, 'form': form})


def post_list(request, board_id):
    if request.method == 'POST':
        board = Board.objects.get(id=board_id)
        Post.objects.create(board=board, title=request.POST['title'], content=request.POST['content'])
        return redirect('/board/'+str(board_id))

    posts = Post.objects.all()

    return render(request, 'post_list.html', {'posts': posts, 'board_id': board_id})


def view_post(request, post_id):
    post_ = Post.objects.get(id=post_id)

    return render(request, 'view_post.html', {'post': post_, 'board_id': request.GET['board']})


def board_list(request):
    board_count = Board.objects.all().count()
    if board_count == 0:
        Board.objects.create(name='Default')

    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})
