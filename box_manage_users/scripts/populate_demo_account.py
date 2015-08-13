# coding: utf-8

from __future__ import unicode_literals
import csv
import os
from box_manage_users.scripts.script import Script


class PopulateDemoAccountScript(Script):
    _title = 'Populate Your Demo Account'
    _message = 'Please follow along with the on-screen instructions.'

    def run(self):
        # Getting folder structure
        self._logger.info(
            '\nAwesome! Let\'s select the parameters of your folder structure.\n'
            'This script will generate a *random* folder structure '
            'unless you enter the same number for the min and max.\n'
        )
        min_depth = raw_input('Minimum depth of folder structure: ')
        max_depth = raw_input('Maximum depth of folder structure: ')
        min_breadth = raw_input('Minimum breadth of each folder: ')
        max_breadth = raw_input('Maximum breadth of each folder: ')

        # Determining which users to create folders & be collabs
        provide_users_switch = raw_input(
            '\nWould you like to provide your own list '
            ' of managed users?\n The alternative is to use '
            'your email address to create fake users.\n'
            '(y/n)'
        )
        if provide_users_switch.lower() == "y" or provide_users_switch.lower() == "yes":
            self._logger.info(
                '\nEnsure the csv with the emails of managed users \n'
                'is in the inputs folder with the name pop_demo.csv'
            )
        else:
            email_address = raw_input(
                '\nIn order to create users, '
                'we will append a plus sign and User# '
                'to the end of your email to create unique aliases. \n'
                'ex: johndoe@box.com --> johndoe+User0@box.com \n'
                'If your email provider does not support this functionality, '
                'please type, "no". \n\n'
                'To continue on with the user creation process, '
                'please provide the email for your demo account:\n'
            )
            if email_address.lower() == 'n' or email_address.lower() == 'no':
                raw_input(
                    '\nType "ready" when the "pop_demo.csv" '
                    'is filled in and placed in the inputs folder.\n'
                )

        # TODO: continue porting the populate_demo script from here!

        super(PopulateDemoAccountScript, self).run()

    def create_user_and_folder(self, email, name, access='editor'):
        """
        Creates a new user and their own personal folder.
        """
        # Log which user script is provisioning in:
        self._overview_logger.info('\n\nEmail: %s - Name: %s', email, name)

        #Create new enterprise user
        new_person = self._client.create_new_user(email, name)
        new_person_id = new_person.id

        #Create own personal folder
        new_person_folder = self._client.create_new_folder(name, '0')
        new_folder_id = new_person_folder.id

        #Add new user as collaborator
        collab = self._client.add_collab(new_folder_id, new_person_id, access)
        new_collab_id = collab.id

        #Update new collab to Owner
        self._client.update_collab(new_collab_id, "owner")

        #Grab new collab_id for the admind,
        my_collab = self._client.get_all_collabs(new_folder_id)
        assert len(my_collab) == 1
        my_collab_id = my_collab[0].id

        #Removed admin collab_id
        self._client.delete_collab(my_collab_id)

        self._logger.info('Success!\n')


def main():
    PopulateDemoAccountScript().run()