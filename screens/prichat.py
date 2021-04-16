from kivy.uix.screenmanager import Screen

from libs.frontend.chat_widget import ChatView
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import ErrorPopup


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

    def on_pre_enter(self, *args):
        try:
            self.display_conversations()
        except DataError as error:
            ErrorPopup(error.message).open()

    def on_leave(self, *args):
        self.ids.prichat_scrollview.clear_widgets()

    def display_conversations(self):
        conversations = self.app.authorized_user.get_conversations()

        for chat_partner in conversations:
            print(chat_partner)
            self.ids.prichat_scrollview.add_widget(
                ChatView(self, chat_partner))