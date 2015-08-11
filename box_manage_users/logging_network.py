# coding: utf-8

from __future__ import unicode_literals
from boxsdk.network.default_network import DefaultNetwork
from pprint import pformat
from box_manage_users.util import setup_logging


class LoggingNetwork(DefaultNetwork):
    """
    SDK Network subclass that logs requests and responses.
    """
    def __init__(self):
        super(LoggingNetwork, self).__init__()
        self._logger = setup_logging()

    def _log_request(self, method, url, **kwargs):
        self._logger.info('%s %s %s', method, url, pformat(kwargs))

    def _log_response(self, response):
        if response.ok:
            self.logger.info(response.content)
        else:
            self._logger.warning('%s\n%s\n%s\n', response.status_code, response.headers, pformat(response.content))

    def request(self, method, url, access_token, **kwargs):
        self._log_request(method, url, **kwargs)
        response = super(LoggingNetwork, self).request(method, url, access_token, **kwargs)
        self._log_response(response)
        return response


from boxsdk.network.default_network import DefaultNetworkResponse


class MockNetworkResponse(DefaultNetworkResponse):
    def json(self):
        return self._request_response

    @property
    def content(self):
        import json
        return json.dumps(self._request_response)

    @property
    def status_code(self):
        return 200

    @property
    def ok(self):
        return True


class MockLoggingNetwork(LoggingNetwork):
    def request(self, method, url, access_token, **kwargs):
        content = {}
        if method == 'DELETE':
            content = None
        else:
            content['id'] = '2015'
        response = MockNetworkResponse(content, access_token)
        self._log_response(response)
        return response
