import re

from unidecode import unidecode


def prepare_text(text: str) -> str:
    text = unidecode(text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace(" ", "")
    return text
