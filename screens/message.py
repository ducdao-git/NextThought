from kivy.uix.screenmanager import Screen

from libs.frontend.chat_widget import UserMessageView, PartnerMessageView
from libs.backend.custom_exception import DataError
from libs.frontend.custom_popup import ErrorPopup


class MessageRoute(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.authorized_user = None
        self.message_partner = None

    def on_pre_enter(self, *args):
        self.authorized_user = self.app.authorized_user
        self.message_partner = self.app.process_message_partner

        self.ids.message_partner_name.text = \
            self.message_partner.get_username()

        self.display_messages()

    def on_leave(self, *args):
        self.ids.message_scrollview.clear_widgets()
        self.ids.message_content_input.text = ''

    def display_messages(self):
        try:
            messages = self.authorized_user.get_messages(
                self.message_partner.get_uid()
            )

            # for loop left out the newest message so we can manually add it
            # and reference for scrollview to scroll to that widget
            for message in messages[:0:-1]:
                if message.get_senderid() == self.authorized_user.get_uid():
                    self.ids.message_scrollview.add_widget(
                        UserMessageView(message.get_content()))
                else:
                    self.ids.message_scrollview.add_widget(
                        PartnerMessageView(message.get_content()))

            # create reference for message view obj
            if messages[0].get_senderid() == self.authorized_user.get_uid():
                newest_msg_view = UserMessageView(messages[0].get_content())
            else:
                newest_msg_view = PartnerMessageView(messages[0].get_content())

            # tell scrollview_widget to scroll to and make sure that message
            # view obj show within the view port.
            # message_scrollview is boxlayout to hold child widget not a
            # scrollview obj -> tell scrollview_widget not message_scrollview.
            self.ids.message_scrollview.add_widget(newest_msg_view)
            self.ids.scrollview_widget.scroll_to(
                newest_msg_view, padding=self.height, animate=True
            )

        except DataError as error:
            ErrorPopup(error.message).open()

    def create_message(self):
        if self.ids.message_content_input.text in ['', None]:
            return

        try:
            self.authorized_user.create_message(
                self.message_partner.get_uid(),
                self.ids.message_content_input.text
            )

            self.ids.message_scrollview.clear_widgets()
            self.display_messages()
            self.ids.message_content_input.text = ''

        except DataError as error:
            ErrorPopup(error.message).open()
