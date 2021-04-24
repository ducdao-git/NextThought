from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from libs.backend.user import AuthorizedUser, create_user
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import ErrorPopup, SuccessSignUpPopup


class SignInInput(BoxLayout):
    """
    structure of the sign in form
    """

    def __init__(self, screen_instance):
        """
        display the empty sign in form
        :param screen_instance: screen obj repr screen display this class
        """
        super().__init__()
        self.screen_instance = screen_instance
        self.user_profile = self.screen_instance.user_profile

        if self.user_profile.get_do_save_auth() == 1:
            self.ids.username_input.text = \
                self.user_profile.get_saved_username()

            self.ids.password_input.text = self.user_profile.get_saved_token()

            self.ids.do_save_auth_checkbox.active = bool(
                self.user_profile.get_do_save_auth())

    def get_signin_data(self):
        """
        :return: return user input data but take out all space on most left and
        right
        """
        return (self.ids.do_save_auth_checkbox.active,
                self.ids.username_input.text.strip(),
                self.ids.password_input.text.strip())

    def clear_input_field(self):
        """
        clear the input field
        """
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''


class SignUpInput(BoxLayout):
    """
    structure of the sign up form
    """

    def __init__(self, screen_instance):
        """
        display the empty sign up form
        :param screen_instance: screen obj repr screen display this class
        """
        super().__init__()
        self.screen_instance = screen_instance

    def get_signup_data(self):
        """
        :return: return user input data but take out all space on most left and
        right
        """
        return self.ids.username_input.text.strip()

    def clear_input_field(self):
        """
        clear the input field
        """
        self.ids.username_input.text = ''


class LoginRoute(Screen):
    """
    screen use to display sign in or sign up input form
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        :param kwargs: param call for Screen class
        """
        super().__init__(**kwargs)
        self.app = app
        self.user_profile = self.app.user_profile
        self.login_action = 'sign_in'
        self.signin_input = None
        self.signup_input = None

    def on_pre_enter(self, *_):
        """
        call display_input_form() when enter to this screen.
        """
        self.display_input_form()

    def on_leave(self, *_):
        """
        set login_action to 'sign_in' when leave the screen. this effect what
        will be display when display_input_form() is called
        """
        self.login_action = 'sign_in'

    def display_input_form(self):
        """
        display input form depend on the login_action sign_in or sign_up form
        will be display
        """
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
        """
        try login with the input data. if unable to login, display error
        """
        if self.login_action == 'sign_in':
            will_saved, username, token = self.signin_input.get_signin_data()

            self.user_profile.switch_do_save_auth(will_saved)

            if username == '' or token == '':
                ErrorPopup(
                    'Both Username and Passwork must be provided.'
                ).open()

                return

            try:
                self.app.authorized_user = AuthorizedUser(username, token)

                self.app.route_manager.transition.direction = 'left'
                self.app.route_manager.current = 'newsfeed_route'

                if will_saved:
                    self.user_profile.set_saved_username(username)
                    self.user_profile.set_saved_token(token)
                else:
                    self.user_profile.set_saved_username('')
                    self.user_profile.set_saved_token('')

                # save user_profile at this point to save password and token
                self.user_profile.save_user_profile()

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
