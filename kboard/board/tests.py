from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from .views import new_post, post_list, view_post
from .models import Post, Board, Comment


class CreatePostPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default')
        super().setUpTestData()

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_new_post_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['board'] = self.default_board.id
        response = new_post(request)

        response_decoded = self.remove_csrf(response.content.decode())
        self.assertIn('settings_id_fields', response_decoded)

    def test_post_list_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'
        request.POST['post_content_text'] = 'NEW POST CONTENT'

        response = post_list(request, self.default_board.id)

        self.assertEqual(Post.objects.count(), 1)
        first_new_post = Post.objects.first()
        self.assertEqual(first_new_post.title, 'NEW POST TITLE')

    def test_new_post_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'
        request.POST['post_content_text'] = 'NEW POST CONTENT'

        response = post_list(request, self.default_board.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/board/'+str(self.default_board.id))

    def test_create_post_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        post_list(request, self.default_board.id)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_list_page_displays_all_list_titles(self):
        Post.objects.create(board=self.default_board, title='turtle1', content='slow')
        Post.objects.create(board=self.default_board, title='turtle2', content='slowslow')

        request = HttpRequest()
        response = post_list(request, self.default_board)

        self.assertIn('turtle1', response.content.decode())
        self.assertIn('turtle2', response.content.decode())


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default')
        super().setUpTestData()

    def test_uses_list_template(self):
        post_ = Post.objects.create(board=self.default_board, title='post of title', content='post of content')
        response = self.client.get('/posts/%d/' % (post_.id,), data={'board': self.default_board.id})
        self.assertTemplateUsed(response, 'view_post.html')

    def test_passes_correct_post_to_template(self):
        other_post = Post.objects.create(
            board=self.default_board,
            title='other post of title',
            content='other post of content'
        )
        correct_post = Post.objects.create(
            board=self.default_board,
            title='correct post of title',
            content='correct post of content'
        )

        response = self.client.get('/posts/%d/' % (correct_post.id,), data={'board': self.default_board.id})

        self.assertEqual(response.context['post'], correct_post)

    def test_view_post_page_displays_correct_title_and_content(self):
        other_post = Post.objects.create(
            board=self.default_board,
            title='other post of title',
            content='other post of content'
        )
        correct_post = Post.objects.create(
            board=self.default_board,
            title='correct post of title',
            content='correct post of content'
        )

        response = self.client.get('/posts/%d/' % (correct_post.id,), data={'board': self.default_board.id})

        self.assertContains(response, 'correct post of title')
        self.assertContains(response, 'correct post of content')
        self.assertNotContains(response, 'other post of title')
        self.assertNotContains(response, 'other post of content')


class PostPaginationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default')
        super().setUpTestData()

    def add_posts(self, post_count):
        for post_counter in range(0, post_count):
            request = HttpRequest()
            request.method = 'POST'
            request.POST['post_title_text'] = 'POST TITLE' + str(post_counter)
            request.POST['post_content_text'] = 'POST CONTENT' + str(post_counter)
            post_counter += 1
            post_list(request, self.default_board.id)

    def test_view_current_page_num(self):
        PostPaginationTest.add_posts(1)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<strong id="current_page_num">1</strong>')

    def test_view_current_page_num(self):
        PostPaginationTest.add_posts(self, 11)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<a class="other_page_num" href="?page=2">2</a>')


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default')
        super().setUpTestData()

    def test_saving_and_retrieving_post(self):
        first_post = Post()
        first_post.board = self.default_board
        first_post.title = 'first post of title'
        first_post.content = 'first post of content'
        first_post.save()

        second_post = Post()
        second_post.board = self.default_board
        second_post.title = 'second post of title'
        second_post.content = 'second post of content'
        second_post.save()

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        first_saved_post = saved_posts[0]
        second_saved_post = saved_posts[1]
        self.assertEqual(first_saved_post.title, 'first post of title')
        self.assertEqual(first_saved_post.content, 'first post of content')
        self.assertEqual(second_saved_post.title, 'second post of title')
        self.assertEqual(second_saved_post.content, 'second post of content')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default')
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )
        super().setUpTestData()

    def test_can_save_a_comment_in_a_particular_post(self):
        Comment.objects.create(post=self.default_post, content='This is a comment')
        saved_posts = Comment.objects.filter(post=self.default_post)

        self.assertEqual(saved_posts.count(), 1)

    def test_can_pass_comment_POST_data(self):
        self.client.post('/comment/new/', data={
            'comment_content': 'This is a comment',
            'post_id': self.default_post.id
        })

        saved_comments = Comment.objects.filter(post=self.default_post)

        self.assertEqual(saved_comments.count(), 1)

    def test_saving_and_retrieving_comment(self):
        second_post = Post.objects.create(
            board=self.default_board,
            title='some post title',
            content='some post content'
        )

        first_comment = Comment()
        first_comment.post = self.default_post
        first_comment.content = 'This is a first comment'
        first_comment.save()

        second_comment = Comment()
        second_comment.post = second_post
        second_comment.content = 'This is a second comment'
        second_comment.save()

        saved_comments = Comment.objects.all()
        self.assertEqual(saved_comments.count(), 2)

        saved_comments_on_default_post = Comment.objects.filter(post=self.default_post)
        saved_comments_on_second_post = Comment.objects.filter(post=second_post)
        self.assertEqual(saved_comments_on_default_post.count(), 1)
        self.assertEqual(saved_comments_on_second_post.count(), 1)

        first_saved_comment = saved_comments[0]
        second_saved_comment = saved_comments[1]
        self.assertEqual(first_saved_comment.content, 'This is a first comment')
        self.assertEqual(second_saved_comment.content, 'This is a second comment')
