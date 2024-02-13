from enum import Enum


class Language(Enum):
    ARABIC = ('arabic', 'ar', 'ar_AR')
    CZECH = ('czech', 'cs', 'cs_CZ')
    GERMAN = ('german', 'de', 'de_DE')
    ENGLISH = ('english', 'en', 'en_XX')
    SPANISH = ('spanish', 'es', 'es_XX')
    ESTONIAN = ('estonian', 'et', 'et_EE')
    FINNISH = ('finnish', 'fi', 'fi_FI')
    FRENCH = ('french', 'fr', 'fr_XX')
    GUJARATI = ('gujarati', 'gu', 'gu_IN')
    HINDI = ('hindi', 'hi', 'hi_IN')
    ITALIAN = ('italian', 'it', 'it_IT')
    JAPANESE = ('japanese', 'ja', 'ja_XX')
    KAZAKH = ('kazakh', 'kk', 'kk_KZ')
    KOREAN = ('korean', 'ko', 'ko_KR')
    LITHUANIAN = ('lithuanian', 'lt', 'lt_LT')
    LATVIAN = ('latvian', 'lv', 'lv_LV')
    BURMESE = ('burmese', 'my', 'my_MM')
    NEPALI = ('nepali', 'ne', 'ne_NP')
    DUTCH = ('dutch', 'nl', 'nl_XX')
    ROMANIAN = ('romanian', 'ro', 'ro_RO')
    RUSSIAN = ('russian', 'ru', 'ru_RU')
    SINHALA = ('sinhala', 'si', 'si_LK')
    TURKISH = ('turkish', 'tr', 'tr_TR')
    VIETNAMESE = ('vietnamese', 'vi', 'vi_VN')
    CHINESE = ('chinese', 'zh', 'zh_CN')
    AFRIKAANS = ('afrikaans', 'af', 'af_ZA')
    AZERBAIJANI = ('azerbaijani', 'az', 'az_AZ')
    BENGALI = ('bengali', 'bn', 'bn_IN')
    PERSIAN = ('persian', 'fa', 'fa_IR')
    HEBREW = ('hebrew', 'he', 'he_IL')
    CROATIAN = ('croatian', 'hr', 'hr_HR')
    INDONESIAN = ('indonesian', 'id', 'id_ID')
    GEORGIAN = ('georgian', 'ka', 'ka_GE')
    KHMER = ('khmer', 'km', 'km_KH')
    MACEDONIAN = ('macedonian', 'mk', 'mk_MK')
    MALAYALAM = ('malayalam', 'ml', 'ml_I')
    MONGOLIAN = ('mongolian', 'mn', 'mn_MN')
    MARATHI = ('marathi', 'mr', 'mr_IN')
    POLISH = ('polish', 'pl', 'pl_PL')
    PASHTO = ('pashto', 'ps', 'ps_AF')
    PORTUGUESE = ('portuguese', 'pt', 'pt_X')
    SWEDISH = ('swedish', 'sv', 'sv_SE')
    SWAHILI = ('swahili', 'sw', 'sw_KE')
    TAMIL = ('tamil', 'ta', 'ta_IN')
    TELUGU = ('telugu', 'te', 'te_IN')
    THAI = ('thai', 'th', 'th_TH')
    TAGALOG = ('tagalog', 'tl', 'tl_XX')
    UKRAINIAN = ('ukrainian', 'uk', 'uk_UA')
    URDU = ('urdu', 'ur', 'ur_PK')
    XHOSA = ('xhosa', 'xh', 'xh_ZA')
    GALICIAN = ('galician', 'gl', 'gl_ES')
    SLOVENE = ('slovene', 'sl', 'sl_SI')

    def __new__(cls, long_language: str = None, short_language: str = None, code: str = None):
        # if long_language is None:

        member = object.__new__(cls)
        member.long_language = long_language
        member.short_language = short_language
        member.code = code
        member._value_ = (long_language, short_language, code)
        return member

    def __str__(self):
        return self.value

    @staticmethod
    def get(value: str = None) -> 'Language':
        for language in Language.list():
            if value in language:
                return Language(language)
        raise ValueError(f'Unknown language: {value}')

    def get_long_language(self):
        return self.long_language

    def get_short_language(self):
        return self.short_language

    def get_code(self):
        return self.code

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
