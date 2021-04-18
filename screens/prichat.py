from kivy.uix.screenmanager import Screen, CardTransition
from time import sleep

from libs.backend.user import ChatPartner
from libs.backend.custom_exception import DataError
from libs.frontend.chat_widget import ChatView
from libs.frontend.custom_popup import ErrorPopup, OneInputFieldPopup


class PriChatRoute(Screen):
    """
    Screen use to display conversations
    """

    def __init__(self, app, **kwargs):
        """
        :param app: current app instance
        """
        super().__init__(**kwargs)
        self.app = app
        self.conversations = None

    def on_pre_enter(self, *args):
        self.display_conversations()

    def on_leave(self, *args):
        self.ids.prichat_scrollview.clear_widgets()

    def display_conversations(self):
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
                    sleep(0.15)
                else:
                    ErrorPopup(error.message).open()

    def find_partner(self):
        OneInputFieldPopup(screen_instance=self,
                           action_name='find_partner').open()

    def get_partner(self, partner_name):
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
