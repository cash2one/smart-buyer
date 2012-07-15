import re
from scrapy.conf import settings
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from scrapy import log
from pyphantomjs import load_page

class JsMiddleware(object):
    def __init__(self):
        self.pattern = re.compile("|".join(settings.get('JS_PATTERNS')))
        log.msg('load JS_PATTERNS: %s' % ",".join(settings.get('JS_PATTERNS')),
                level=log.INFO)

    def process_request(self, request, spider):
        if self.pattern.match(request.url):
            (rc, url, content) = load_page(request.url, timeout=30)  
            if rc != 0:
                raise IgnoreRequest(
                    'pyphantomjs error, rc:%s, url:%s, content:%s'%\
                    (rc, url, content))
            else:
                log.msg('pyphantomjs run %s' % url)
                response = HtmlResponse(url=url, body=content, encoding='utf-8')
                return response