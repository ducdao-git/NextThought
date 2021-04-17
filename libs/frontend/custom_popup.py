from kivy.uix.modalview import ModalView


class FilterPopup(ModalView):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.root = root

        if self.root.filter_username not in ['', None]:
            self.ids.filter_username.text = self.root.filter_username

        if self.root.filter_tag not in ['', None]:
            self.ids.filter_tag.text = self.root.filter_tag

    def on_dismiss(self):
        filter_username, filter_tag = None, None

        if self.ids.filter_username.text != '':
            filter_username = self.ids.filter_username.text

        if self.ids.filter_tag.text != '':
            filter_tag = self.ids.filter_tag.text

        self.root.filter_post(filter_username, filter_tag)


class OneInputFieldPopup(ModalView):
    def __init__(self, root=None, postview_instance=None,
                 action_name='create_post', **kwargs):
        super().__init__(**kwargs)
        self.postview_instance = postview_instance
        self.root = root
        self.action_name = action_name

        if action_name == 'edit_post':
            self.ids.post_content_popup_title.text = 'Edit post'
            self.ids.post_content_input.text = \
                self.postview_instance.post.get_content()

        elif action_name == 'create_post':
            self.ids.post_content_input.text = ''

        elif action_name in ['edit_comment', 'edit_top_comment']:
            self.ids.post_content_popup_title.text = 'Edit post'
            self.ids.post_content_input.text = \
                self.postview_instance.comment.get_content()

    def on_dismiss(self):
        if self.action_name == 'edit_post':
            self.postview_instance.post_edit(self.ids.post_content_input.text)

        elif self.action_name == 'create_post':
            self.root.create_post(self.ids.post_content_input.text)

        elif self.action_name == 'edit_top_comment':
            self.postview_instance.top_comment_edit(
                self.ids.post_content_input.text)

        elif self.action_name == 'edit_comment':
            self.postview_instance.comment_edit(
                self.ids.post_content_input.text)


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
