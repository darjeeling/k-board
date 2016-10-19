from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def check_for_row_in_list_table(self, id, row_text):
        table = self.browser.find_element_by_id(id)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, "".join([row.text for row in rows]))

    def test_default_page(self):
        # 지훈이는 멋진 게시판 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Board List'를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Board List', self.browser.title)
        self.assertIn('Board List', header_text)

        # 게시판 목록에 'Default' 게시판이라고 씌여져 있다.
        self.check_for_row_in_list_table('id_board_list_table', 'Default')

        # 지훈이는 첫 번째에 있는 'Default'게시판에 들어간다.
        self.move_to_default_board()

        # 게시판에 아무런 글이 없다.
        tbody = self.browser.find_element_by_tag_name('tbody')
        with self.assertRaises(NoSuchElementException):
            tbody.find_element_by_tag_name('tr')

        # 지훈이는 다른 게시판이 있나 보려고 게시판 목록 버튼을 눌러 게시판 목록 페이지로 돌아간다.
        board_list_button = self.browser.find_element_by_id('board_list_button')
        board_list_button.click()

        self.assertRegex(self.browser.current_url, '.+/$')

        self.check_for_row_in_list_table('id_board_list_table', 'Default')

        # Default 게시판 밖에 없어서 글을 쓰려고 게시판을 누른다.
        default_board = self.browser.find_element_by_css_selector('table#id_board_list_table a')
        default_board.click()

    def test_write_post_and_confirm_post_view(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 글 쓰기 페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/default/new/')

        # 웹 페이지 타이틀과 헤더가 'Create Post'를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Create Post', self.browser.title)
        self.assertIn('Create Post', header_text)

        # 제목을 입력하는 상자에 'Insert Title'라고 씌여 있다.
        titlebox = self.browser.find_element_by_id('id_new_post_title')
        self.assertEqual(
            titlebox.get_attribute('placeholder'),
            'Insert Title'
        )

        # "Title of This Post"라고 제목 상자에 입력한다.
        titlebox.send_keys('Title of This Post')

        contentbox = self.get_contentbox()

        # "Content of This Post"라고 본문 상자에 입력한다.
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()

        # 하단의 등록 버튼을 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        self.click_submit_button()
        self.assertRegex(self.browser.current_url, '.+/default/')

        # 게시글 목록 페이지의 타이틀에 'Post list'라고 씌여져 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Post list', self.browser.title)
        self.assertIn('Post list', header_text)

        # 게시글 목록에 "1: Title of This Post"라고 씌여져 있다.
        self.check_for_row_in_list_table('id_post_list_table', 'Title of This Post')

        # 게시글 목록 하단에 있는 '글쓰기' 버튼을 눌러서 새 글을 작성한다.
        self.click_create_post_button()

        # "Title of Second Post"라고 제목 상자에 입력한다.
        titlebox = self.browser.find_element_by_id('id_new_post_title')
        titlebox.send_keys('Title of Second Post')

        # "Content of Second Post"라고 본문 상자에 입력한다
        contentbox = self.get_contentbox()
        contentbox.send_keys('Content of Second Post')
        self.browser.switch_to.default_content()

        # 하단의 등록 버든틍 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        self.click_submit_button()
        self.assertRegex(self.browser.current_url, '.+/default/')

        # 게시글 목록에 두 개의 게시글 제목이 보인다.
        self.check_for_row_in_list_table('id_post_list_table', 'Title of Second Post')
        self.check_for_row_in_list_table('id_post_list_table', 'Title of This Post')

        # 지훈이는 게시글이 잘 작성 되었는지 확인하고 싶어졌다.
        # '1: Title of This Post' 게시글을 클릭한다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_css_selector('tbody > tr > td > a')
        rows[0].click()

        # 게시글에 대한 자세한 내용을 보여주는 새로운 창이 뜬다.
        self.assertRegex(self.browser.current_url, '.+/default/(\d+)/')

        # 게시글 페이지의 타이틀에는 'View Post'라고 씌여져 있다.
        self.assertIn('View Post', self.browser.title)

        # 게시글의 제목에는 'Title of This Post'이 표시되고
        post_title = self.browser.find_element_by_css_selector('.post-panel .panel-title').text
        self.assertIn('Title of This Post', post_title)

        # 게시글의 내용에는 'Content of This Post'이 표시된다.
        post_content = self.browser.find_element_by_css_selector('.post-panel .panel-body').text
        self.assertIn('Content of This Post', post_content)

        # 지훈이는 게시글 내용 하단의 댓글 란에 'This is a comment'라고 입력한다.
        comment = self.browser.find_element_by_id('id_new_comment')
        comment.send_keys('This is a comment')

        # '댓글 달기' 버튼을 누른다.
        comment_submit = self.browser.find_element_by_id('id_new_comment_submit')
        comment_submit.click()

        # 댓글이 달리고, 'This is a comment'라는 댓글이 보인다.
        comment_list = self.browser.find_element_by_id("id_comment_list")
        comments = comment_list.find_elements_by_css_selector('a > h4')
        self.assertEqual(comments[0].text, 'This is a comment')

        # 게시글과 댓글이 잘 작성된 것을 확인한 지훈이는 다시 게시글 목록을 보여주는 페이지로 돌아가기 위해 게시글 하단의 '목록' 버튼을 누른다.
        create_post_button = self.browser.find_element_by_id('id_back_to_post_list_button')
        create_post_button.click()

        # 게시글 목록 페이지가 뜬다.
        self.assertRegex(self.browser.current_url, '.+/default/$')
