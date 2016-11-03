from urllib.parse import urlencode

from .base import BoardAppTest
from board.templatetags.url_parameter import url_parameter


class UrlParameterTest(BoardAppTest):
    def test_contains_correct_string(self):
        parameter = {
            'a': 13,
            'query': 'hello',
            'b': 'This is a test'
        }
        url_string = url_parameter(**parameter)

        self.assertEqual(urlencode(parameter), url_string)
