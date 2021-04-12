from kivy.uix.modalview import ModalView


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
        self.ids.message_label.text = message
