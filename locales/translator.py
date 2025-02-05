from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner
from fluent_compiler.bundle import FluentBundle
import os


class Translator:
    t_hub: TranslatorHub

    def __init__(self):
        self.t_hub = TranslatorHub(
            {
                "en": ("en", "ru",),
                "ru": ("ru",)
            },
            [
                FluentTranslator(
                    locale="en",
                    translator=FluentBundle.from_files("en-US",
                                                       filenames=[os.path.abspath("./locales/locales/en.ftl")])
                ),
                FluentTranslator(
                    locale="ru",
                    translator=FluentBundle.from_files("ru-Ru",
                                                       filenames=[os.path.abspath("./locales/locales/ru.ftl")])
                )
            ], root_locale="ru"
        )

    def __call__(self, language, *args, **kwargs):
        return LocalizedTranslator(
            translator=self.t_hub.get_translator_by_locale(locale=language)
        )


class LocalizedTranslator:
    translator: TranslatorRunner

    def __init__(self, translator: TranslatorRunner):
        self.translator = translator

    def get(self, key: str, **kwargs) -> str:
        return self.translator.get(key, **kwargs)
