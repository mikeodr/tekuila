=============
tekuila
=============

"Have you had to much to download?"

.. image:: https://travis-ci.org/mikeodr/tekuila.svg?branch=master
    :target: https://travis-ci.org/mikeodr/tekuila

Pull your TekSavvy Quota and act on it.

To avoid using command line flags create a config file at::

    ~/.tekuila

Place the following variables within the config file::

    API=<your API KEY from https://myaccount.teksavvy.com/ApiKey/ApiKeyManagement>
    CAP=<your cap in GB>
    WARN_RATIO=<ratio % to warn in 0.1 increments up to 1.0>

Installation
============

To install, run the following::

    pip install tekuila

Or, if you wish to install the latest from source::

    git clone https://github.com/mikeodr/tekuila
    cd tekuila
    python setup.py install

License
=======
GPLv2
