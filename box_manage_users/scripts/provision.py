# coding: utf-8

from __future__ import unicode_literals
from boxsdk.exception import BoxAPIException
import csv
import os
from box_manage_users.scripts.script import Script


class MassProvisionScript(Script):
    """
    Script to create many users in an enterprise at once.
    """
    _title = 'Provision Users & Create Personal Folders'
    _message = 'Ensure that the csv file is in the inputs folder with the name input_users.csv'

    def run(self):
        """
        Base class override.
        Open the input_users.csv and create a user for each name/email in the file.
        """
        with open(os.path.join('inputs', 'input_users.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                iterrow = iter(row)
                for item in iterrow:
                    name = item
                    email = next(iterrow)
                    self.create_user_and_folder(email, name, 'co-owner')
        super(MassProvisionScript, self).run()

    def create_user_and_folder(self, email, name, access='editor'):
        """
        Creates a new user and their own personal folder.
        """
        # Log which user script is provisioning in:
        self._overview_logger.info('\n\nEmail: %s - Name: %s', email, name)

        #Create new enterprise user
        try:
            new_person = self._client.create_new_user(email, name)
        except BoxAPIException as ex:
            self._fail_logger.warning('Could not create user {} ({}) - {}'.format(name, email, ex))
            return

        new_person_id = new_person.id

        #Create own personal folder
        new_person_folder = self._client.create_new_folder(name, '0')
        new_folder_id = new_person_folder.id

        #Add new user as collaborator
        collab = self._client.add_collab(new_folder_id, new_person_id, access)
        new_collab_id = collab.id

        #Update new collab to Owner
        self._client.update_collab(new_collab_id, "owner")

        #Grab new collab_id for the admin
        my_collab = self._client.get_all_collabs(new_folder_id)
        assert len(my_collab) == 1
        my_collab_id = my_collab[0].id

        #Removed admin collab_id
        self._client.delete_collab(my_collab_id)

        self._logger.info('Success!\n')


def main():
    MassProvisionScript().run()


if __name__ == '__main__':
    main()
