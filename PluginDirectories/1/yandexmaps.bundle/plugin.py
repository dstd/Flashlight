# coding=UTF-8
import urllib
import json
import i18n
import unicodedata

def results(fields, original_query):
    query = fields['~query']
    query = unicodedata.normalize("NFC", query).encode('UTF-8')
    search_url = "https://yandex.ru/maps/?z=18&mode=search&text=" + urllib.quote_plus(query)

    return {
        "title": search_url,
        "run_args": [search_url],
        "html": """
            <script>
            setTimeout(function() {
                window.location = %s
            }, 200);
            </script>
        """ % (json.dumps(search_url)),
        "webview_user_agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)",
        "webview_links_open_in_browser": True
    }


def run(url):
    import os
    os.system("open '{0}'".format(url))
