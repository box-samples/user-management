Box Tech Consulting Scripts
===========================

About
-----

This is a collection of scripts written to aid the Box Tech Consulting organization to manage users in an enterprise.


Installation
------------

To install, simply:

.. code-block:: console

    git clone https://github.com/box-samples/user-management.git
    cd user-management
    python setup.py install


Using the Scripts
-----------------

These scripts assume you have set up a Box developer account and have created a Box application.
The scripts will ask you for information about the application, including your client ID, client secret, and
developer token.

Go to to https://box-content.readme.io/v2.0/docs/oauth-20 to help find your developer credentials.

Once you have followed the installation instructions, you will have the following scripts available in your path.

- box-provision - Create many user accounts in your enterprise.
- box-deprovision - Remove many user accounts in your enterprise.
- box-populate-demo-account - Create a random folder structure in your account.


Compatibility
-------------

The user management scripts were written in Python 2.7 and have not yet been tested in other Python versions.


Contributing
------------

See `CONTRIBUTING.rst <https://github.com/box-samples/user-management/blob/master/CONTRIBUTING.rst>`_.


Setup
~~~~~

Create a virtual environment and install packages -

.. code-block:: console

    mkvirtualenv box-user-management
    pip install -r requirements.txt
