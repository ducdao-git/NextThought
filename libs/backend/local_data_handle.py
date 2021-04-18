import json
from datetime import datetime, timedelta
from dateutil import tz

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
