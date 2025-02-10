from __future__ import annotations

from json import dumps, loads
from logging import info
from typing import TYPE_CHECKING

import aiofiles
from aiopath import Path
from discord import Locale
from discord.app_commands import (
    Translator,
    locale_str,
    TranslationContext,
)


if TYPE_CHECKING:
    from .client import Void


async def translate(client: Void) -> str:
    raise NotImplementedError


class TranslationEngine(Translator):
    def __init__(self, client: Void) -> None:
        super().__init__()
        self.cache: dict[str, dict[str, str]] = {}
        self.missing: dict[str, str] = {}
        self.client: Void = client

    async def create_translation_file_if_not_exists(self, locale: str) -> None:
        if not await Path(f"src/translations/{locale}.json").exists():
            async with aiofiles.open(f"src/translations/{locale}.json", "w+", encoding="utf8") as file:
                await file.write("{}")

    async def cache_translations(self) -> None:
        translated_for: list[str] = self.client.config.get("bot", "translation_locales").split(" | ")
        for locale in translated_for:
            await self.create_translation_file_if_not_exists(locale)
            async with aiofiles.open(f"src/translations/{locale}.json", "r", encoding="utf8") as file:
                r: str = await file.read()
                if "{" not in r:
                    async with aiofiles.open(f"src/translations/{locale}.json", "w+", encoding="utf8") as file:
                        r = "{}"
                        await file.write(r)
                self.cache[locale] = loads(r)

        translation_ct: int = len([string for locale in self.cache.values() for string in locale.values()])
        info(f"cached {translation_ct} translations")

    async def translate(
        self,
        string: locale_str,
        locale: Locale,
        context: TranslationContext,  # type: ignore
    ) -> str | None:
        original_text = str(string)
        # translation files are stored in src/locales as json files
        # the file name is the locale name

        lang: str

        match locale:
            case Locale.british_english | Locale.american_english:
                lang = "en"
            case _:  # not supported
                return original_text

        if original_text in self.cache[lang]:
            return self.cache[lang][original_text]

        # write missing translation to json file
        if lang not in self.missing:
            self.missing[original_text] = lang

        # dump {actual: actual} to lang.json
        async with aiofiles.open(f"src/translations/{lang}.json", "r", encoding="utf8") as file:
            data: dict[str, str] = loads(await file.read())
        data[original_text] = original_text
        async with aiofiles.open(f"src/translations/{lang}.json", "w+", encoding="utf8") as file:
            r: str = dumps(data, indent=4)
            await file.write(r)

        return original_text
