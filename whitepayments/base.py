# coding=utf-8

import six

from . import WHITE_API_KEY
from . import WHITE_OPEN_API_KEY


class CommunicationException(Exception): pass


class WhiteException(Exception): pass


class Request(object):
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = WHITE_API_KEY
        self._api_key = api_key

    def get(self, url, headers):
        try:
            response = requests.get(
                url, headers=headers, timeout=60, allow_redirects=True,
                auth=requests.auth.HTTPBasicAuth(self._api_key, ''))
            content, status_code = response.content, response.status_code
        except Exception as e:
            self._handle_error(e)
        else:
            return (content.json(), status_code)

    def post(self, url, headers, data=None):
        headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
        try:
            response = requests.post(
                url, headers=headers, data=data, timeout=60, allow_redirects=True,
                auth=requests.auth.HTTPBasicAuth(self._api_key, ''))
            content, status_code = response.content, response.status_code
        except Exception as e:
            self._handle_error(e)
        else:
            return (content.json(), status_code)

    def put(self, url, headers, data=None):
        headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
        try:
            response = requests.put(
                url, headers=headers, data=data, timeout=60, allow_redirects=True,
                auth=requests.auth.HTTPBasicAuth(self._api_key, ''))
            content, status_code = response.content, response.status_code
        except Exception as e:
            self._handle_error(e)
        else:
            return (content.json(), status_code)

    def _handle_error(self, error):
        err = '{0}: {1}'.format(type(error).__name__, six.text_type(error))

        raise CommunicationException(err)


class ResourceBase(object):
    def __init__(self, data=None):
        if data:
            self._data = data
        else:
            self._data = {}

    @classmethod
    def _handle_error(self, error):
        raise WhiteException(error)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError


