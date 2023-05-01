from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ReplyKeyboardMarkup, Message

from src.i18n import _ as gettext, fake_gettext  # noqa
from src.i18n import __ as lazygettext  # noqa


_ = fake_gettext


class _TextKeyIcon:

    def __init__(self, text: str, default_icon: str = "•") -> None:
        self.text: str = text
        self.icon: str = default_icon

    def __call__(self, icon: str = "") -> '_TextKeyIcon':
        self.icon = icon
        return self

    def __str__(self) -> str:
        return f"{gettext(self.text)} {self.icon}"

    @classmethod
    def extract_text(cls, text: str) -> str:
        text = text.split(" ")[:-1]
        return " ".join(text)


class TextKeys:
    # Global
    MAIN_MENU: _TextKeyIcon = _TextKeyIcon(_("button_main_menu"))

    # Exercises
    FIND_EXERCISE: _TextKeyIcon = _TextKeyIcon(_("button_find_exercise"), default_icon="🔎")
    GET_PROGRAM: _TextKeyIcon = _TextKeyIcon(_("button_get_program"))
    GET_INDIVIDUAL_PROGRAM: _TextKeyIcon = _TextKeyIcon(_("button_get_individual_program"))

    # Admin
    ADMIN_PANEL: _TextKeyIcon = _TextKeyIcon(_("button_admin_panel"))
    ADD_EXERCISE: _TextKeyIcon = _TextKeyIcon(_("button_add_exercise"))
    ADD_CURRENT_WEEK_PROGRAM: _TextKeyIcon = _TextKeyIcon(_("button_add_current_week_program"))
    ADD_NEXT_WEEK_PROGRAM: _TextKeyIcon = _TextKeyIcon(_("button_add_next_week_program"))
    ADD_INDIVIDUAL_PROGRAM: _TextKeyIcon = _TextKeyIcon(_("button_add_individual_program"))


class TextKeyBuilder(ReplyKeyboardMarkup):

    def add(self, *args: _TextKeyIcon):
        args = (str(item) for item in args)
        super(TextKeyBuilder, self).add(*args)


class TextKeyFilter(BoundFilter):
    key: str = "text_key"

    def __init__(self, text_key: '_TextKeyIcon'):
        self.text_key: _TextKeyIcon = text_key

    async def check(self, message: Message) -> bool:

        return _TextKeyIcon.extract_text(message.text) == lazygettext(self.text_key.text)
