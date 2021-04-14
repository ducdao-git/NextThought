from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.graphics import Color, Rectangle

from libs.custom_kv_widget import IconButton


class PostOptionButton(IconButton):
    def __init__(self, postview_instance, option_action, **kwargs):
        super().__init__(**kwargs)
        self.option_action = option_action
        self.postview_instance = postview_instance

        if option_action == 'edit':
            option_icon = self.edit_icon
        elif option_action == 'delete':
            option_icon = self.delete_icon
        else:
            option_icon = self.error_icon

        self.text = f'[size=16sp]{option_icon}[/size]'

    def on_release(self):
        if self.option_action == 'edit':
            return self.postview_instance.post_edit()
        elif self.option_action == 'delete':
            return self.postview_instance.post_delete()
        else:
            return None


class PostInfoButton(Button):
    def __init__(self, owner_name, posted_time, **kwargs):
        super().__init__(**kwargs)
        self.text = f"[b]{owner_name}[/b]\n[size=12sp][color=" \
                    f"{self.posted_time_color}]{posted_time}[/color][/size]"

        self.bind(size=self.update_text_size)
        self.bind(texture_size=self.update_height)

    def update_text_size(self, *args):
        """
        update value of text_size. this function make sure the text_size not
        take widget default/initial size as the value
        """
        self.text_size = self.width, None

    def update_height(self, *args):
        """
        update value of widget height. this function make sure the height not
        take widget default/initial texture_size as the value
        """
        self.height = self.texture_size[1]


class PostContentButton(Button):
    def __init__(self, post_content, **kwargs):
        super().__init__(**kwargs)
        self.text = post_content

        self.bind(size=self.update_text_size)
        self.bind(texture_size=self.update_height)

    def update_text_size(self, *args):
        """
        update value of text_size. this function make sure the text_size not
        take widget default/initial size as the value
        """
        self.text_size = self.width, None

    def update_height(self, *args):
        """
        update value of widget height. this function make sure the height not
        take widget default/initial texture_size as the value
        """
        self.height = self.texture_size[1]


class PostDividerLabel(Label):
    """
    custom label with height 1 to act as divider
    """

    def __init__(self, **kwargs):
        """
        create a label to act as a divider
        """
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(rgba=self.color)
            self.rect = Rectangle()

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """
        update position and size of rectangle in the canvas instruction. this
        function make sure canvas not take widget default position and size
        """
        self.rect.pos = self.pos
        self.rect.size = self.size


class PostView(BoxLayout):
    """
    custom boxlayout to display a public post
    """

    def __init__(self, root, post, **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.post = post

        self.ids.row.add_widget(
            PostInfoButton(self.post.get_owner_name(), self.post.get_time()))

        if self.root.app.authorized_user.get_username() == \
                self.post.get_owner_name():
            self.ids.row.add_widget(PostOptionButton(self, 'edit'))
            self.ids.row.add_widget(PostOptionButton(self, 'delete'))

        self.add_widget(PostContentButton(self.post.get_content()))
        self.add_widget(PostDividerLabel())

        self.bind(minimum_height=self.setter('height'))

    def post_edit(self):
        print('edit post')

    def post_delete(self):
        print('delete post')
        self.post.delete_public_post(self.root.app.authorized_user)
        self.root.delete_post(self)
