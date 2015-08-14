# coding: utf-8

from __future__ import unicode_literals
from boxsdk import Client
from boxsdk.config import API
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.user import User
import json
from box_manage_users.logging_network import LoggingNetwork
from box_manage_users.tc_oauth2 import TCOAuth2
from box_manage_users.util import log_on_success, setup_logging


class TCClient(Client):
    """
    Box SDK Client subclass with additional methods useful for user and collab management.
    """
    def __init__(self, oauth=None, network_layer=None, session=None):
        oauth = oauth or TCOAuth2()
        super(TCClient, self).__init__(oauth, network_layer=LoggingNetwork(), session=session)

    @log_on_success('Got the current user.')
    def get_current_user(self):
        return self.user().get()

    @log_on_success('Got all users in the current enterprise.')
    def get_all_users(self, filter_term):
        url = '{0}/users'.format(API.BASE_API_URL)
        box_response = self._session.get(url, params={'filter_term': filter_term, 'limit': 1000})
        response = box_response.json()
        return [User(self._session, item['id'], item) for item in response['entries']]

    @log_on_success('Got user with ID {user_id}.')
    def get_user(self, user_id):
        return self.user(user_id).get()

    @log_on_success('Created user named {name} with email {email}.')
    def create_new_user(self, email, name):
        return self.create_user(name, email)

    @log_on_success('Deleted user with ID {user_id}.')
    def delete_user(self, user_id):
        return self.user(user_id).delete()

    @log_on_success('Transferred root folder ownership from {user_id} to {transfer_user_id}.')
    def move_users_folder(self, user_id, transfer_user_id):
        url = '{}/users/{}/folders/0'.format(API.BASE_API_URL, user_id)
        data = json.dumps({'owned_by': transfer_user_id})
        return self.make_request('PUT', url, data=data)

    @log_on_success('Created new folder under {parent_id} named {name}.')
    def create_new_folder(self, name, parent_id):
        return self.folder(parent_id).create_subfolder(name)

    @log_on_success('User {user_id} is now a(n) {access} of folder {folder_id}.')
    def add_collab(self, folder_id, user_id, access='editor'):
        return self.folder(folder_id).add_collaborator(self.user(user_id), access)

    @log_on_success('Got all collabs for folder {folder_id}.')
    def get_all_collabs(self, folder_id):
        url = self.folder(folder_id).get_url('collaborations')
        response = self.make_request('GET', url)
        return [Collaboration(self._session, r['id'], r) for r in response.json()['entries']]

    @log_on_success('Updated collaboration with ID {collab_id}. New role: {new_role}.')
    def update_collab(self, collab_id, new_role):
        collab = Collaboration(self._session, collab_id)
        url = collab.get_url()
        data = {'role': new_role}
        self._session.put(url, data=json.dumps(data), expect_json_response=False)
        # TODO: remove above code and replace with below when Box API correctly returns the updated collab
        # return Collaboration(self._session, collab_id).update_info(new_role)

    @log_on_success('Removed collaboration with ID {collab_id}.')
    def delete_collab(self, collab_id):
        return Collaboration(self._session, collab_id).delete()

    def get_user_by_email(self, email):
        users = self.get_all_users(email)
        if not users:
            return None
        return users[0]
