# coding=UTF-8
import urllib
import json
import os
import re

langs = {
    'auto': 'Any',
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azeerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ny': 'Nyanja (Chichewa)',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese (Portugal, Brazil)',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala (Sinhalese)',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tl': 'Tagalog (Filipino)',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu' }

def fix_lang_shortcut(lang):
    if len(lang) < 2:
        return lang
    lang = lang.lower()

    fixups = {'cn':'zh-CN', 'tw':'zh-TW'}
    if lang in fixups:
        return fixups[lang]
    
    for code, name in langs.items():
        if name.lower().startswith(lang):
            return code
            
    return lang
    
def results(args, original_query):
    url = 'https://translate.google.com/m/translate#<LANG_FROM>/<LANG_TO>/<TEXT>'

    if args.get('~lang') == None:
        lang_from = original_query[4:6]
        lang_to = original_query[6:8]
        if original_query[8:9] != ' ':
            return
        args['~lang'] = "%s-%s" % (lang_from, lang_to)
    else:
        match = re.search('gtr (.+) to (.+)', original_query) # workaround to match greedy
        args = { '~text': match.group(1), '~lang': match.group(2) }
        
    text = args.get('~text', '').encode('UTF-8')
    lang = args.get('~lang', '').encode('UTF-8')

    if ' ' in lang:
        return {
            "title": "Google Translate",
            "html": ""
        }

    lang = lang.split('-')
    if len(lang) == 2:
        from_lang = fix_lang_shortcut(lang[0])
        from_lang_name = langs.get(from_lang)
        to_lang = fix_lang_shortcut(lang[1])
        to_lang_name = langs.get(to_lang)
        title = "Translate %s → %s" % (from_lang_name, to_lang_name)
    elif len(lang) == 1:
        from_lang = 'auto'
        from_lang_name = langs.get(from_lang)
        to_lang = fix_lang_shortcut(lang[0])
        to_lang_name = langs.get(to_lang)
        title = "Translate to %s" % (to_lang_name)
    elif len(lang) == 0:
        return
    else:
        from_lang = ''
        to_lang = ''

    if from_lang_name == None:
        return {
            "title": "Google Translate",
            "html": "%s: <b>%s</b>" % ("Invalid source language specified", from_lang)
        }

    if to_lang_name == None:
        return {
            "title": "Google Translate",
            "html": "%s: <b>%s</b>" % ("Invalid target language specified", to_lang)
        }

    url = url.replace('<LANG_FROM>', from_lang)
    url = url.replace('<LANG_TO>', to_lang)
    url = url.replace('<TEXT>', urllib.quote_plus(text))

    return {
        "title": title,
        "run_args": [url],
        "html": "<script>setTimeout(function() { window.location = %s }, 500)</script>" % json.dumps(url),
        "webview_user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
        "webview_links_open_in_browser": True
    }


def run(url):
    os.system('open "{0}"'.format(url.replace('/m/translate', '/')))

# EOF
