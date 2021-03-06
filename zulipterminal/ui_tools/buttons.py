from typing import Any, Dict, List

import urwid


class MenuButton(urwid.Button):
    def __init__(self, caption: Any, email: str='') -> None:
        self.caption = caption  # str
        self.email = email
        super(MenuButton, self).__init__("")
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'    ', self.caption], 0), None, 'selected')


class HomeButton(urwid.Button):
    def __init__(self, controller: Any, count: int=0) -> None:
        self.caption = 'All messages'
        self.count = count
        super(HomeButton, self).__init__("")
        self._w = self.widget(count)
        urwid.connect_signal(self, 'click', controller.show_all_messages)

    def update_count(self, count: int) -> None:
        self.count = count
        self._w = self.widget(count)

    def widget(self, count: int) -> Any:
        if count <= 0:
            count = ''  # type: ignore
        return urwid.AttrMap(urwid.SelectableIcon(
            [u'  \u26FA  ', self.caption, ('idle', ' ' + str(count))],
            len(self.caption) + 5),
            None,
            'selected')


class PMButton(urwid.Button):
    def __init__(self, controller: Any, count: int=0) -> None:
        self.caption = 'Private messages'
        super(PMButton, self).__init__("")
        self.count = count
        self._w = self.widget(count)
        urwid.connect_signal(self, 'click', controller.show_all_pm)

    def update_count(self, count: int) -> None:
        self.count = count
        self._w = self.widget(count)

    def widget(self, count: int) -> Any:
        if count <= 0:
            count = ''  # type: ignore
        return urwid.AttrMap(urwid.SelectableIcon(
            [u'  \u260F  ', self.caption, ('idle', ' ' + str(count))],
            len(self.caption) + 5),
            None,
            'selected')


class StreamButton(urwid.Button):
    def __init__(self, properties: List[Any],
                 controller: Any, view: Any, count: int=0) -> None:
        self.caption = properties[0]
        self.stream_id = properties[1]
        color = properties[2]
        self.color = color[:2] + color[3] + color[5]
        view.palette['default'].append((self.color, '', '', '', self.color,
                                       'black'))
        self.count = count
        super(StreamButton, self).__init__("")
        self._w = self.widget(count)
        urwid.connect_signal(self, 'click', controller.narrow_to_stream)
        urwid.connect_signal(self, 'click', view.write_box.stream_box_view)

    def update_count(self, count: int) -> None:
        self.count = count
        self._w = self.widget(count)

    def widget(self, count: int) -> Any:
        if count <= 0:
            count = ''  # type: ignore
        return urwid.AttrMap(urwid.SelectableIcon(
            [(self.color, u'  # '), self.caption, ('idle', ' ' + str(count))],
            len(self.caption) + 4),
            None,
            'selected')


class UserButton(urwid.Button):
    def __init__(self, user: Dict[str, Any], controller: Any,
                 view: Any, color: str=None, count: int=0) -> None:
        self.caption = user['full_name']  # str
        self.email = user['email']
        self.user_id = user['user_id']
        self.color = color
        self.count = count
        self.recipients = frozenset({
            self.user_id, view.model.user_id})
        super(UserButton, self).__init__("")
        self._w = self.widget(count)
        urwid.connect_signal(self, 'click', controller.narrow_to_user)
        urwid.connect_signal(self, 'click',
                             view.write_box.private_box_view)

    def update_count(self, count: int) -> None:
        self.count = count
        self._w = self.widget(count)

    def widget(self, count: int) -> Any:
        if count <= 0:
            count = ''  # type: ignore
        return urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET}  ', self.caption, ('idle', ' ' + str(count))],
            len(self.caption) + 5),
            self.color,
            'selected')
