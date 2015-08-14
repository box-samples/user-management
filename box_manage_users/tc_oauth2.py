# coding: utf-8

from __future__ import unicode_literals
from boxsdk import OAuth2


class TCOAuth2(OAuth2):
    """
    Box SDK OAuth2 subclass.
    Allows for interactively asking the user for auth credentials.
    When using a developer token, allows "refresh" of that token by interactively asking for a new one.
    """
    def __init__(
            self,
            client_id=None,
            client_secret=None,
            store_tokens=None,
            box_device_id='0',
            box_device_name='',
            access_token=None,
            refresh_token=None,
            network_layer=None,
    ):
        if client_id is None or client_secret is None or access_token is None:
            print 'To start we need your credentials for the developer account.'
            print 'Go to to https://box-content.readme.io/v2.0/docs/oauth-20 to help find your developer credentials.'

        if client_id is None:
            client_id = raw_input('Please enter your client id: ')
        if client_secret is None:
            client_secret = raw_input('Please enter your client secret: ')
        if access_token is None:
            access_token = raw_input('Please enter your access/developer token: ')
        if refresh_token is None:
            refresh_token = raw_input('Please enter your refresh token (leave blank if using a developer token): ')
            if not refresh_token:
                refresh_token = None
        super(TCOAuth2, self).__init__(
            client_id,
            client_secret,
            store_tokens,
            box_device_id,
            box_device_name,
            access_token,
            refresh_token,
            network_layer,
        )

    def _refresh(self, access_token):
        """
        Base class override. If the user hasn't supplied a refresh token, just ask the user for a new access token.
        """
        if self._refresh_token is not None:
            return super(TCOAuth2, self)._refresh(access_token)
        else:
            self._access_token = raw_input('Developer token has expired. Please get a new one and enter it here: ')
            return self._access_token, self._refresh_token
