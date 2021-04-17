from time import sleep

from kivy.uix.screenmanager import Screen

from libs.backend.local_data_handle import get_readable_time
from libs.backend.custom_exception import DataError
from libs.frontend.chat_widget import UserMessageView, PartnerMessageView
from libs.frontend.custom_popup import ErrorPopup


class MessageRoute(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.authorized_user = None
        self.message_partner = None
        # self.scrollview_height = 0
        # self.message_scrollview_height = 0

        # self.ids.scrollview_widget.bind(
        #     height=self.get_scrollview_height)

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

            if len(messages) == 0:
                return

            # for loop left out the newest message so we can manually add it
            # and reference for scrollview to scroll to that widget
            for message in messages[:0:-1]:
                if message.get_senderid() == self.authorized_user.get_uid():
                    self.ids.message_scrollview.add_widget(
                        UserMessageView(
                            message.get_content(),
                            get_readable_time(message.get_time(), True)
                        ))
                else:
                    self.ids.message_scrollview.add_widget(
                        PartnerMessageView(
                            message.get_content(),
                            get_readable_time(message.get_time(), True)
                        ))

            # create reference for message view obj
            if messages[0].get_senderid() == self.authorized_user.get_uid():
                newest_msg_view = UserMessageView(
                    messages[0].get_content(),
                    get_readable_time(messages[0].get_time(), True)
                )
            else:
                newest_msg_view = PartnerMessageView(
                    messages[0].get_content(),
                    get_readable_time(messages[0].get_time(), True)
                )

            # tell scrollview_widget to scroll to and make sure that message
            # view obj show within the view port.
            # message_scrollview is boxlayout to hold child widget not a
            # scrollview obj -> tell scrollview_widget not message_scrollview.
            self.ids.message_scrollview.add_widget(newest_msg_view)
            self.ids.scrollview_widget.scroll_to(
                newest_msg_view, padding=self.height, animate=True
            )

            # self.ids.message_scrollview.bind(
            #     minimum_height=self.get_message_scrollview_height)
            #
            # height_diff = self.scrollview_height - self.message_scrollview_height
            # if height_diff > 0:
            #     # print(height_diff)
            #     self.ids.message_scrollview.add_widget(
            #         Label(size_hint=(1, None), height=height_diff),
            #         index=len(messages)
            #     )

        except DataError as error:
            if error.message == \
                    'Too many requests. Please try again later.':
                sleep(0.05)
                self.display_messages()
            else:
                ErrorPopup(error.message).open()

    # def get_message_scrollview_height(self, _, height):
    #     print(height)
    #     self.message_scrollview_height = height
    #
    # def get_scrollview_height(self, _, scrollview_height):
    #     self.scrollview_height = scrollview_height

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
