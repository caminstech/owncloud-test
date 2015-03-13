# owncloud-test

## Python environment setup

    $ sudo apt-get install python-virtualenv
    $ virtualenv owncloud-test --no-site-packages --python=/usr/bin/python3
    $ cd owncloud-test
    $ source bin/activate
    $ easy_install -U setuptools
    $ easy_install nose mockito requests urllib3 flask humanfriendly
