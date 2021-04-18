import json
from datetime import datetime, timedelta
from dateutil import tz

from pprint import pprint

from libs.backend.custom_exception import DataError


def _hex_to_rgb(hex_color):
    """
    :param hex_color: valid hex code of a color
    :return: rgba value each between 0 and 1
    """
    hex_color = hex_color.lstrip('#')
    hex_color = list(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    result = []
    for value in hex_color:
        result.append(round(value / 255, 3))

    result.append(1.0)

    return result


def get_theme_palette(theme_name):
    """
    get color data of the theme_name
    :param theme_name: name of the theme - next_mess
    :return: color palette for the theme
    """
    try:
        if theme_name not in ['next_mess', 'dark']:
            raise ValueError

        with open('assets/theme_palettes.json', 'r') as f:
            themes_data = json.load(f)

        theme_data = themes_data[theme_name]
        theme_palette = {}

        for color in theme_data:
            if color in ['support_text_color', 'good_color']:
                theme_palette[color] = theme_data[color]
            else:
                theme_palette[color] = _hex_to_rgb(theme_data[color])

        # pprint(theme_palette)
        return theme_palette

    except Exception as error:
        raise DataError(error)


def get_readable_time(time, message_time=False):
    try:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        post_utc_time = datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S'
        ).replace(tzinfo=from_zone)

        post_local_time = post_utc_time.astimezone(to_zone)
        curr_time = datetime.now().astimezone(to_zone)
        time_diff = curr_time - post_local_time

        if message_time:
            if (time_diff / timedelta(days=365)) > 1:
                return post_local_time.strftime('%b %d, %Y AT %H:%M')
            else:
                return post_local_time.strftime('%b %d AT %H:%M')

        elif (time_diff / timedelta(days=365)) > 1:
            return post_local_time.strftime('%x')
        elif (time_diff / timedelta(days=1)) > 1:
            return post_local_time.strftime('%b %d')
        elif (time_diff / timedelta(hours=1)) > 1:
            return str(time_diff.seconds // 3600) + 'h'
        elif (time_diff / timedelta(minutes=1)) > 1:
            return str(time_diff.seconds // 60) + 'm'
        else:
            return str(time_diff.seconds) + 's'

    except Exception as error:
        print(f'error ppost get_time: {error}')
        raise DataError(error)


class UserProfile:
    def __init__(self):
        try:
            with open('user_profile.json', 'r') as infile:
                self.user_profile = json.load(infile)

            pprint(self.user_profile)

        except Exception as error:
            raise DataError(error)

    def get_theme_name(self):
        return self.user_profile['theme_name']

    def get_remember_username(self):
        return self.user_profile['remember_username']

    def get_remember_token(self):
        return self.user_profile['remember_token']

    def get_num_post_show(self):
        return self.user_profile['num_post_show']

    def get_num_message_show(self):
        return self.user_profile['num_message_show']

    def set_theme_name(self, new_theme_name):
        self.user_profile['theme_name'] = new_theme_name

    def set_remember_username(self, new_remember_username):
        self.user_profile['remember_username'] = new_remember_username

    def set_remember_token(self, new_remember_token):
        self.user_profile['remember_token'] = new_remember_token

    def set_num_post_show(self, new_num_post_show):
        if new_num_post_show.isdigit():
            new_num_post_show = int(new_num_post_show)
        else:
            raise DataError('Number of Post Show must be integer')

        if new_num_post_show < 1:
            raise DataError('Number of Post Show must be a positive'
                            ' integer (number > 0)')
        elif new_num_post_show > 100:
            raise DataError(
                'Number of Post Show cannot excess 100 (number < 101)'
            )

        self.user_profile['num_post_show'] = new_num_post_show

    def set_num_message_show(self, new_num_message_show):
        if new_num_message_show.isdigit():
            new_num_message_show = int(new_num_message_show)
        else:
            raise DataError('Number of Message Show must be integer')

        if new_num_message_show < 1:
            raise DataError('Number of Message Show must be a positive'
                            ' integer (number > 0)')
        elif new_num_message_show > 100:
            raise DataError(
                'Number of Message Show cannot excess 100 (number < 101)'
            )

        self.user_profile['num_message_show'] = new_num_message_show

    def save_user_profile(self):
        try:
            with open('user_profile.json', 'w') as outfile:
                json.dump(self.user_profile, outfile, indent=2)
        except Exception as error:
            raise DataError(error)
