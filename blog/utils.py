# utils.py

import requests

LIBRETRANSLATE_URL = 'http://localhost:5000/translate'  # Replace with your LibreTranslate instance URL

def translate_text(text, source_lang, target_lang):
    params = {
        'q': text,
        'source': source_lang,
        'target': target_lang
    }
    
    response = requests.get(LIBRETRANSLATE_URL, params=params)
    translated_text = response.json()[0][0]['translatedText']
    
    return translated_text
