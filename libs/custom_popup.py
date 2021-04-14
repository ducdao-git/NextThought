from kivy.uix.modalview import ModalView


class SearchPopup(ModalView):
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


class PostEditPopup(ModalView):
    def __init__(self, postview_instance, **kwargs):
        super().__init__(**kwargs)
        self.postview_instance = postview_instance
        self.ids.post_edit_new_content.text = \
            self.postview_instance.post.get_content()

    def on_dismiss(self):
        self.postview_instance.post_new_content = \
            self.ids.post_edit_new_content.text
        self.postview_instance.post_edit()


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
