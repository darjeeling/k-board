from django.test import TestCase
from board.models import Post, Board, Comment


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
