from .base import FunctionalTest


class RegistrationFormTest(FunctionalTest):
    def test_two_passwords_are_correct(self):
        # 혜선이는 회원가입을 하고싶어한다.
        self.browser.get(self.live_server_url + '/accounts/register/')

        # 가입에 필요한 정보를 작성한다.
        self.register_send_key("id_username", "chickenlover01")
        self.register_send_key("id_email", "chsun0303@naver.com")
        self.register_send_key("id_password1", "abcd0000")
        self.register_send_key("id_fullName", "testfullname")

        # 손이 미끄러져서 똑같은 비밀번호를 치지못했다.
        self.register_send_key("id_password2", "abcd0009")

        checkbox = self.browser.find_element_by_id("id_terms")
        checkbox.click()

        self.click_submit_button()

        # Password 아래 쪽에 두 비밀번호가 같지않다고 에러메시지가 나온다.
        error = self.browser.find_element_by_class_name("errorlist")
        self.assertTrue("The two password fields didn't match.", error)

    # TODO
    # password가 abcd1234와 같이 너무 흔한 경우 일 때 에러메시지 띄우기
    # db에 username이 이미 있으면 에러메시지 띄우기
