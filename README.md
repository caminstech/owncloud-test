# owncloud-test

## Python environment setup

    $ sudo apt-get install python-virtualenv
    $ virtualenv owncloud-test --no-site-packages --python=/usr/bin/python3
    $ cd owncloud-test
    $ source bin/activate
    $ easy_install -U setuptools
    $ easy_install nose mockito requests urllib3 flask humanfriendly
    
## Server

Example.

    $ ./app.py --testname test-files/example.test --new-database --database database.db --logfile=server.log
    
## Clients

    $ ./app.py --baseurl=http://SERVER_ADDRESS:5000 --clientid=CLIENT_ID
