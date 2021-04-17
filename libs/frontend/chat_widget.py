from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import CardTransition
from kivy.uix.label import Label

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from libs.backend.custom_exception import DataError
from libs.backend.local_data_handle import get_readable_time
from libs.frontend.custom_popup import ErrorPopup


class ChatView(BoxLayout):
    def __init__(self, screen_instance, chat_partner, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.app = self.screen_instance.app
        self.authorized_user = self.screen_instance.app.authorized_user
        self.chat_partner = chat_partner

        last_message = self.authorized_user.get_messages(
            self.chat_partner.get_uid(), limit=1
        )[0]

        self.ids.chat_partner_name.text = self.chat_partner.get_username()

        if last_message.get_senderid() == self.authorized_user.get_uid():
            self.ids.last_message_preview.text = \
                'You: ' + last_message.get_content()
        else:
            self.ids.last_message_preview.text = last_message.get_content()

        self.ids.last_message_time.text = \
            get_readable_time(last_message.get_time())

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.collide_point(*touch.opos):
            self.app.process_message_partner = self.chat_partner

            self.app.route_manager.transition = \
                CardTransition(direction='left')
            self.app.route_manager.current = 'message_route'
            self.app.route_manager.return_route = 'prichat_route'


class MessageContentLabel(Label):
    def __init__(self, message_content, partner=False, **kwargs):
        super().__init__(**kwargs)
        self.text = message_content

        if partner:
            self.background_color = self.partner_bg_color
            self.color = self.partner_text_color

        with self.canvas.before:
            Color(rgba=self.background_color)
            self.rect = RoundedRectangle()

        self.bind(pos=self.update_rect, size=self.update_rect)

        # must use bind to get correct/updated value of attribute
        self.bind(texture_size=self.update_text_size)
        self.bind(size=self.update_rect)

    def update_text_size(self, *_):
        # once update self.text_size will automatically update texture_size
        # and since self.size = self.texture_size in our case (in .kv),
        # this will also update the widget size automatically.

        if self.texture_size[0] > dp(300):
            self.text_size = dp(300), None
        else:
            self.text_size = self.texture_size[0], None

    def update_rect(self, *_):
        """
        update position and size of rectangle in the canvas instruction. this
        function make sure canvas not take widget default position and size
        """
        self.rect.pos = self.pos
        self.rect.size = self.size


class UserMessageView(BoxLayout):
    def __init__(self, message_content, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(
            MessageContentLabel(message_content, pos_hint={'right': 1}))


class PartnerMessageView(BoxLayout):
    def __init__(self, message_content, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MessageContentLabel(message_content, partner=True))
