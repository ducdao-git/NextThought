from kivy.uix.modalview import ModalView


class FilterPopup(ModalView):
    def __init__(self, screen_instance, **kwargs):
        super().__init__(**kwargs)
        self.screen_instance = screen_instance

        if self.screen_instance.filter_username not in ['', None]:
            self.ids.filter_username.text = self.screen_instance.filter_username

        if self.screen_instance.filter_tag not in ['', None]:
            self.ids.filter_tag.text = self.screen_instance.filter_tag

    def on_dismiss(self):
        filter_username, filter_tag = None, None

        if self.ids.filter_username.text != '':
            filter_username = self.ids.filter_username.text

        if self.ids.filter_tag.text != '':
            filter_tag = self.ids.filter_tag.text

        self.screen_instance.filter_post(filter_username, filter_tag)


class OneInputFieldPopup(ModalView):
    def __init__(self, screen_instance=None, view_instance=None,
                 action_name='create_post', **kwargs):
        super().__init__(**kwargs)
        self.view_instance = view_instance
        self.screen_instance = screen_instance
        self.action_name = action_name

        if action_name == 'edit_post':
            self.ids.popup_title.text = 'Edit post'
            self.ids.input_field.text = \
                self.view_instance.post.get_content()

        elif action_name == 'create_post':
            self.ids.input_field.text = ''

        elif action_name in ['edit_comment', 'edit_top_comment']:
            self.ids.popup_title.text = 'Edit post'
            self.ids.input_field.text = \
                self.view_instance.comment.get_content()

        elif action_name == 'find_partner':
            self.size_hint = (0.7, 1)
            self.ids.popup_title.text = 'Stat conversation with'
            self.ids.input_icon.text = self.user_icon
            self.ids.input_field.hint_text = 'Type a username...'

    def on_dismiss(self):
        if self.action_name == 'edit_post':
            self.view_instance.post_edit(self.ids.input_field.text)

        elif self.action_name == 'create_post':
            self.screen_instance.create_post(self.ids.input_field.text)

        elif self.action_name == 'edit_top_comment':
            self.view_instance.top_comment_edit(
                self.ids.input_field.text)

        elif self.action_name == 'edit_comment':
            self.view_instance.comment_edit(
                self.ids.input_field.text)

        elif self.action_name == 'find_partner':
            self.screen_instance.get_partner(
                self.ids.input_field.text)


class ErrorPopup(ModalView):
    """
    custom error popup
    """

    def __init__(self, message, **kwargs):
        """
        create a popup with this message
        :param message: string as message will be display
        """
        super().__init__(**kwargs)
        self.ids.error_popup_message.text = message
