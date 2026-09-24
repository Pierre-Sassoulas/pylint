import gettext


class C:
    def __init__(self, translation: gettext.NullTranslations) -> None:
        self.translation = translation

    @property
    def gettext(self) -> None:
        return None
