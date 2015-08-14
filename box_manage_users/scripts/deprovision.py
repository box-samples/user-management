# coding: utf-8

from __future__ import unicode_literals
import csv
import os
from box_manage_users.scripts.script import Script


class MassDeprovisionScript(Script):
    _title = 'Deprovision Users'
    _message = 'Ensure that the csv file is in the inputs folder with the name input_emails.csv'

    def run(self):
        archive_email = raw_input('Please enter the email of the account you\'d like the data to be transferred to: ')

        with open(os.path.join('inputs', 'input_emails.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                iterrow = iter(row)
                for email in iterrow:
                    self._logger.debug("Email: " + email)
                    self.delete_user(email, archive_email)
        super(MassDeprovisionScript, self).run()

    def delete_user(self, email, archive_email):
        # Log which user script is provisioning in:
        self._overview_logger.info('\n\nEmail: %s - Moving content to: %s', email, archive_email)

        # Grab id associated with user's email
        user_id = self.get_user_id_from_email_address(email)
        # Grab id associated with the archive email
        archive_id = self.get_user_id_from_email_address(archive_email)

        # If either id could not be found, gracefully exit subroutine
        if user_id is None or archive_id is None:
            print "Failed at some point. Check logs for more info.\n"
            return

        # Move content from original owner to archive owner
        self._client.move_users_folder(user_id, archive_id)

        # Move deletes user
        self._client.delete_user(user_id)

        self._logger.info('Success!\n')


def main():
    MassDeprovisionScript().run()


if __name__ == '__main__':
    main()
