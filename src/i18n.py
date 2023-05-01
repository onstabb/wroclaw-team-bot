from aiogram.contrib.middlewares.i18n import I18nMiddleware


from src.config import I18N_DOMAIN, LOCALE_DIR, DEFAULT_LANGUAGE

i18n: I18nMiddleware = I18nMiddleware(I18N_DOMAIN, LOCALE_DIR, default=DEFAULT_LANGUAGE)
_ = i18n.gettext
__ = i18n.lazy_gettext


def fake_gettext(string: str) -> str:
    """This required for string parser"""
    return string




