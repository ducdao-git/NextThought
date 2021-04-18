from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from libs.backend.user import AuthorizedUser, create_user
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import ErrorPopup, SuccessSignUpPopup


class SignInInput(BoxLayout):
    def __init__(self, screen_instance):
        super().__init__()
        self.screen_instance = screen_instance

    def get_signin_data(self):
        return self.ids.username_input.text.strip(), \
               self.ids.password_input.text.strip()

    def clear_input_field(self):
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''


class SignUpInput(BoxLayout):
    def __init__(self, screen_instance):
        super().__init__()
        self.screen_instance = screen_instance

    def get_signup_data(self):
        return self.ids.username_input.text.strip()

    def clear_input_field(self):
        self.ids.username_input.text = ''


class LoginRoute(Screen):
    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app
        self.login_action = 'sign_in'
        self.signin_input = None
        self.signup_input = None

    def on_pre_enter(self, *args):
        self.display_input_form()

    def display_input_form(self):
        self.signin_input = SignInInput(self)
        self.signup_input = SignUpInput(self)

        self.ids.input_field_holder.clear_widgets()

        if self.login_action == 'sign_in':
            self.ids.input_field_holder.add_widget(self.signin_input)

            self.ids.signin_button.bg_color = self.primary_color
            self.ids.signin_button.color = self.text_primary_color

            self.ids.signup_button.bg_color = self.support_color
            self.ids.signup_button.color = self.text_support_color

            self.ids.login_button.text = f'{self.signin_icon}  Sign In'

        elif self.login_action == 'sign_up':
            self.ids.input_field_holder.add_widget(self.signup_input)

            self.ids.signin_button.bg_color = self.support_color
            self.ids.signin_button.color = self.text_support_color

            self.ids.signup_button.bg_color = self.primary_color
            self.ids.signup_button.color = self.text_primary_color

            self.ids.login_button.text = f'{self.signup_icon}  Create Account'

    def try_login(self):
        if self.login_action == 'sign_in':
            username, token = self.signin_input.get_signin_data()

            if username == '' or token == '':
                ErrorPopup(
                    'Both Username and Passwork must be provided.'
                ).open()

                return

            try:
                self.app.authorized_user = AuthorizedUser(username, token)

                self.app.route_manager.transition.direction = 'left'
                self.app.route_manager.current = 'newsfeed_route'

            except DataError as error:
                ErrorPopup(error.message).open()

        elif self.login_action == 'sign_up':
            username = self.signup_input.get_signup_data()

            if username == '':
                ErrorPopup(
                    'A Username must be provided.'
                ).open()

                return

            try:
                self.app.authorized_user = create_user(username)

                SuccessSignUpPopup(
                    self, self.app.authorized_user.get_token()).open()

                self.signin_input.clear_input_field()
                self.signup_input.clear_input_field()

            except DataError as error:
                ErrorPopup(error.message).open()
