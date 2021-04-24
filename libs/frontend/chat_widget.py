from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import CardTransition
from kivy.uix.button import Button

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle


class ChatView(BoxLayout):
    """
    class use to display individual user who has conversation with authorized
    user in the prichat screen
    """

    def __init__(self, screen_instance, chat_partner, **kwargs):
        """
        create a new chat view
        :param screen_instance: Screen obj repr screen this class object will
        be display on
        :param chat_partner: ChatPartner obj repr user who has conversation
        with authorized user
        :param kwargs: param call for BoxLayout class
        """
        super().__init__(**kwargs)
        self.screen_instance = screen_instance
        self.app = self.screen_instance.app
        self.authorized_user = self.screen_instance.app.authorized_user
        self.chat_partner = chat_partner

        """
        # display last message in prichat screen but will increase prichat 
        # screen load time
        
        from libs.backend.local_data_handle import get_readable_time
        
        last_message = self.authorized_user.get_messages(
            self.chat_partner.get_uid(), limit=1
        )[0]

        if last_message.get_senderid() == self.authorized_user.get_uid():
            self.ids.last_message_preview.text = \
                'You: ' + last_message.get_content()
        else:
            self.ids.last_message_preview.text = last_message.get_content()

        self.ids.last_message_time.text = \
            get_readable_time(last_message.get_time())
        """

        self.ids.chat_partner_name.text = self.chat_partner.get_username()
        self.ids.chat_info_holder.remove_widget(self.ids.last_message_preview)

    def on_touch_up(self, touch):
        """
        if touch in this class instance move to message screen with this
        AuthorizedUser and ChatPartner
        :param touch: touch obj for touch position
        """
        if self.collide_point(*touch.pos) and self.collide_point(*touch.opos):
            self.app.process_message_partner = self.chat_partner

            self.app.route_manager.transition = \
                CardTransition(direction='left')
            self.app.route_manager.current = 'message_route'
            self.app.route_manager.return_route = 'prichat_route'


class MessageContentLabel(Button):
    """
    class use to display a message and show message sent time when press
    """

    def __init__(self, message_content, partner=False, **kwargs):
        """
        create a new MessageContentLabel, display differently if message sent
        by AuthorizedUser vs sent by ChatPartner
        :param message_content: string repr content of the message
        :param partner: boolean repr if this message post by partner
        :param kwargs: param call for Button class
        """
        super().__init__(**kwargs)
        self.text = message_content

        if partner:
            self.background_color = self.partner_bg_color
            self.color = self.partner_text_color

        with self.canvas.before:
            Color(rgba=self.background_color)
            self.rect = RoundedRectangle()

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.background_color = (0, 0, 0, 0)

        # must use bind to get correct/updated value of attribute
        self.bind(texture_size=self.update_text_size)
        self.bind(size=self.update_rect)

    def update_text_size(self, *_):
        """
        update kivy text_size for the widget
        """
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

    def on_release(self):
        """
        when the instance get clicked, display message sent time
        """
        if self.parent.ids.message_send_time.text == '':
            self.parent.ids.message_send_time.text = \
                f'--  {self.parent.message_time}  --'
        else:
            self.parent.ids.message_send_time.text = ''


class UserMessageView(BoxLayout):
    """
    class use to display message sent by AuthorizedUser
    """

    def __init__(self, message_content, message_time, **kwargs):
        """
        :param message_content: string repr content of the message
        :param message_time: string repr sent time of the message
        :param kwargs: param call for BoxLayout class
        """
        super().__init__(**kwargs)
        self.message_time = message_time

        self.add_widget(
            MessageContentLabel(message_content, pos_hint={'right': 1})
        )


class PartnerMessageView(BoxLayout):
    """
    class use to display message sent by ChatPartner
    """

    def __init__(self, message_content, message_time, **kwargs):
        """
        :param message_content: string repr content of the message
        :param message_time: string repr sent time of the message
        :param kwargs: param call for BoxLayout class
        """
        super().__init__(**kwargs)
        self.message_time = message_time

        self.add_widget(MessageContentLabel(message_content, partner=True))
