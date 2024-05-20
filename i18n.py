from locales import en, ru

translations = {
    "en": en.translations,
    "ru": ru.translations,
}

current_language = "ru"

def set_language(language):
    global current_language
    if language in translations:
        current_language = language

def translate(message_id):
    return translations[current_language].get(message_id, message_id)
