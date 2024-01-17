# Some asynchronous functions for text formatting.
import asyncio
import string
from typing import Literal

from asyncstdlib import any_iter
from transliterate import translit


async def replace_whitespace(text: str, new_symbol: str = '_') -> str:
    """
    Replaces all tab, line feed, return, form feed, and vertical tab characters with the new character.
    :param text: Source string.
    :param new_symbol: Replacement Symbol. The default is '_'.
    :return: New edited string.
    :raises ValueError: If argument type 'text' or 'new_symbol' is not str.
    """

    if not isinstance(text, str) or not isinstance(new_symbol, str):
        raise TypeError

    new_text = ''
    a_text = any_iter(text)  # get an asynchronous iterator.
    async for t in a_text:
        if t in string.whitespace:
            new_text = new_text + new_symbol
        else:
            new_text += t

    return new_text


async def del_punctuation(text: str) -> str:
    """Removes punctuation marks from the string."""
    if not isinstance(text, str):
        raise TypeError
    return ''.join(filter(lambda s: s not in string.punctuation, text))


async def translit_ru_en(text: str, reverse: bool = False) -> str:
    """
    Replaces Russian characters with English characters and vice versa.
    :param text: Source text.
    :param reverse: If True, it replaces Latin characters with Cyrillic.
                    If False, it replaces Russian characters with Latin characters.
    :return: New string.
    :raises ValueError: If argument type 'text' is not str.
    """
    if not isinstance(text, str):
        raise TypeError
    return translit(text, language_code='ru', reversed=reverse)


async def name_formatter(name: str,
                         punctuation_del: bool = False,
                         translit_text: Literal['ru-en', 'en-ru'] | None = None,
                         replace_space: str | None = None,
                         ) -> str:
    """
    Formats the name for its future use in paths, url, slags, etc.
    The order in which the argument commands are checked and processed, if set:

    1.punctuation_del

    2.translit_text

    3.replace_space
    :param name: Source text
    :param translit_text: If 'ru-en replaces Russian characters with Latin characters.
                          If 'en-ru' replaces Latin characters with Russian characters.
                          If None doesn't do anything. Default None
    :param replace_space: If None, performs no action.
                          If str, replaces all tab, line feed, return, form feed and vertical tab characters with
                          a new character. Dfault None
    :param punctuation_del: If True removes punctuation marks. Default False
    :return: Formatted Name.
    :raises TypeError: If argument type 'name' is not str.
    """
    if not isinstance(name, str):
        raise TypeError

    new_name = name

    if punctuation_del:
        new_name = await del_punctuation(new_name)

    if translit_text is not None:
        if translit_text == 'ru-en':
            new_name = await translit_ru_en(new_name, reverse=True)
        elif translit_text == 'en-ru':
            new_name = await translit_ru_en(new_name)
        else:
            raise ValueError("The argument 'translit_text' must be the literal 'ru-en' or 'en-ru' or None.")

    if replace_space is not None:
        if isinstance(replace_space, str):
            new_name = await replace_whitespace(new_name, new_symbol=replace_space)
        else:
            raise TypeError

    return new_name

