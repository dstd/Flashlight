# coding=UTF-8
import urllib
import json
import os

def fix_lang_shortcut(lang):
    return {'cn':'zh-CN', 'tw':'zh-TW'}.get(lang, lang)

def results(parsed, original_query):
    url = 'https://translate.google.com/m/translate#<LANG_FROM>/<LANG_TO>/<TEXT>'

    if parsed.get('~lang') == None:
        lang_from = original_query[4:6].encode('UTF-8')
        lang_to = original_query[6:8].encode('UTF-8')
        if original_query[8:9] != ' ':
            return
        parsed['~lang'] = "%s%s" % (lang_from, lang_to)

    text = parsed.get('~text', '').encode('UTF-8')
    lang = parsed.get('~lang', '').encode('UTF-8').split('-')
    
    if len(lang) == 4:
        from_lang = fix_lang_shortcut(lang[0:2])
        to_lang = fix_lang_shortcut(lang[2:4])
        title = "Translate %s → %s" % (from_lang, to_lang)
    elif len(lang) == 2:
        from_lang = 'auto'
        to_lang = fix_lang_shortcut(lang)
        title = "Translate to %s" % (lang)
    elif
        return

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
