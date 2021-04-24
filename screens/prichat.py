from kivy.uix.screenmanager import Screen, CardTransition
from time import sleep

from libs.backend.user import ChatPartner
from libs.backend.custom_exception import DataError
from libs.frontend.chat_widget import ChatView
from libs.frontend.custom_popup import ErrorPopup, SettingPopup
from libs.frontend.custom_popup import OneInputFieldPopup


class PriChatRoute(Screen):
    """
    screen use to display users with which our authorized user has had
    conversations
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        :param kwargs: param call for Screen class
        """
        super().__init__(**kwargs)
        self.app = app
        self.conversations = None

    def on_pre_enter(self, *_):
        """
        call display_conversations() when the transition to this screen start
        """
        self.display_conversations()

    def on_leave(self, *_):
        """
        empty the screen scrollview when leave the screen
        """
        self.ids.prichat_scrollview.clear_widgets()

    def display_conversations(self):
        """
        display all users with which authorized user has had conversations.
        include auto retry if request code is 429 (too many request) or open
        error popup if some other DataError catch
        """
        try:
            self.conversations = self.app.authorized_user.get_conversations()
        except DataError as error:
            ErrorPopup(error.message).open()
            return

        partner_index = 0
        conversations_num = len(self.conversations)

        while partner_index < conversations_num:
            try:
                self.ids.prichat_scrollview.add_widget(
                    ChatView(self, self.conversations[partner_index])
                )
                partner_index += 1

            except DataError as error:
                if error.custom_code == 429:
                    sleep(0.1)
                else:
                    ErrorPopup(error.message).open()

    def find_partner(self):
        """
        open popup allow user to enter a username
        """
        OneInputFieldPopup(screen_instance=self,
                           action_name='find_partner').open()

    def get_partner(self, partner_name):
        """
        find user with partner_name. if found, open the message screen with
        that user. if not found, display the error
        :param partner_name: string repr name of a user
        """
        if partner_name in ['', None]:
            return

        try:
            new_chat_partner = ChatPartner(partner_name)
            self.app.process_message_partner = new_chat_partner

            self.app.route_manager.transition = \
                CardTransition(direction='left')
            self.app.route_manager.current = 'message_route'
            self.app.route_manager.return_route = 'prichat_route'

        except DataError as error:
            ErrorPopup(error.message).open()

    def open_setting_popup(self):
        """
        open setting popup
        """
        SettingPopup(self).open()
