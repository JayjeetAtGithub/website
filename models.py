from http.cookies import SimpleCookie

DEFAULT_ENCODING = "utf-8"


class HttpRequest:

    def __init__(self, environ, *args, **kwargs):
        self._environ = environ

    @property
    def method(self):
        return self._environ['REQUEST_METHOD'].lower()

    @property
    def environ(self):
        return self._environ

    @property
    def path(self):
        return self._environ['PATH_INFO']

    @path.setter
    def path(self, path):
        self._environ['PATH_INFO'] = path 

    @property
    def headers(self):
        header_query = 'HTTP_'
        header_dict = {}
        for key, value in self._environ.items():
            if key.startswith(header_query):
                header_dict[key] = value
        return header_dict

    @property
    def cookies(self):
        parsed_cookies = SimpleCookie(self.headers.get('Cookie'))
        cookies_dict = {}
        for k, v in parsed_cookies.items():
            cookies_dict[k] = v.value
        return cookies_dict

    @property
    def mimetype(self):
        self.headers.get("Content-Type")

    @property
    def get_full_url(self):
        raw_uri = self._environ['RAW_URI']
        http_host = self._environ['HTTP_HOST']
        return (http_host + raw_uri[1:]).lower()


class HttpResponse:

    default_status = "200 OK"
    default_mimetype = "text/plain"

    def __init__(self, content=None, *args, **kwargs):
        self._content = content  # Bytes representation of response body
        self._mimetype = self.default_mimetype
        self._status = self.default_status
        self._headers = {}
        self._encoding = DEFAULT_ENCODING

    @property
    def mimetype(self):
        return self._mimetype

    @property
    def status(self):
        return self._status

    @property
    def content(self):
        return self._content.encode("utf-8")

    @property
    def headers(self):
        return self._headers

    @mimetype.setter
    def mimetype(self, val):
        self._mimetype = val

    @status.setter
    def status(self, val):
        self._status = val

    def update_headers(self, key, value):
        self._headers[key] = value



