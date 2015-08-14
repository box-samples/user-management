# coding: utf-8

from __future__ import unicode_literals
import os
from py.io import TerminalWriter
from box_manage_users.tc_client import TCClient
from box_manage_users.util import setup_logging


class Script(object):
    """
    Script base class.
    Configures logging and outputs duck ascii art.
    """
    _title = 'Base Script'
    _message = 'Instructions'
    _verbose_log_filename = os.path.join('logs', 'verbose.log')
    _failure_log_filename = os.path.join('logs', 'failure.log')
    _overview_log_filename = os.path.join('logs', 'overview.log')

    def __init__(self):
        self._logger = setup_logging(name='console')
        self._tw = TerminalWriter()
        self._tw.sep('#', self._title, green=True, bold=True)
        self._client = TCClient()
        self._logger.info(
            'Great! Let\'s get this going!\n'
            '    		_      _      _\n'
            '      >(.)__ <(.)__ =(.)__\n'
            '       (___/  (___/  (___/ \n'
        )
        self._verbose_logger = setup_logging(self._verbose_log_filename, debug=True)
        self._fail_logger = setup_logging(self._failure_log_filename, name='failures')
        self._overview_logger = setup_logging(self._overview_log_filename, name='overview')

    def run(self):
        """
        Runs the script. Intended to be overridden by base classes.
        """
        self._tw.sep('#', 'Process Complete!', green=True, bold=True)

    def get_user_id_from_email_address(self, email):
        """
        Given an email address, find the user in the enterprise that has that email address and return that user's id.
        :param email: User's email address for which to retrieve the user ID.
        :return: The user ID of the user with the given email address.
        """
        user = self._client.get_user_by_email(email)
        if user is None:
            self._fail_logger.warning('No user with login %s. Could not deprovision.', email)
            self._overview_logger.warning('No user with login %s. Could not deprovision.', email)
            return None
        return user.id
