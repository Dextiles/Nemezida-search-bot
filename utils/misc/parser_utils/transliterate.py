from transliterate import translit


def transliterate_en(text_str):
    return translit(text_str, 'ru', reversed=True)
