import os
from json import loads, dumps
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


class APIMixin(object):

    def setUp(self):
        """"""

    def request(self, method, url_path, data=None):
        url = urljoin(os.environ.get('DEV_SERVER', 'http://localhost:8000'), url_path)
        print()

        kwargs = {'method': method}

        if data is not None:
            kwargs['data'] = bytes(dumps(data), encoding='utf8')
            kwargs['headers'] = {'content-type': 'application/json'}

        req = Request(url, **kwargs)
        try:
            with urlopen(req) as resp:
                data = resp.read().decode('utf-8')
        except HTTPError as e:
            print('Error code: ', e.code)
            resp = e
        except URLError as e:
            print('Reason: ', e.reason)
            resp = e
        data = loads(data) if data else data

        print(resp.status, resp.reason, data)
        return resp, data

    def verify_item(self, data, **kwargs):
        self.assertEqual(data['key'], self.key)
        self.assertEqual(data['active'], kwargs.get('active', True))
        return data

    def api_create(self, view, **kwargs):
        resp, data = self.request('POST', view.get_url(), data=kwargs)
        self.assertEqual(resp.status, 201)
        return self.verify_item(data, **kwargs)

    def api_update(self, view, **kwargs):
        resp, data = self.request('POST', view.get_url(), data=kwargs)
        self.assertEqual(resp.status, 200)
        return self.verify_item(data, **kwargs)

    def api_get(self, view, http_status=200):
        resp, data = self.request('GET', view.get_url())
        self.assertEqual(resp.status, http_status)

        return data

    def api_list(self, url):
        return self.request('GET', url)

    def api_error(self, func, code, *args, **kwargs):
        try:
            data = func(*args, **kwargs)
            self.fail('Dead Code')
        except HTTPError as e:
            print(e)
            self.assertEqual(e.code, code)
