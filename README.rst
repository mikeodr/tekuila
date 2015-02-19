tekuila
=============

Interface for querying your TekSavvy download quota
"Have you had to much to download?"

.. image:: https://pypip.in/v/tekuila/badge.png
        :target: https://pypi.python.org/pypi/tekuila/
        :alt: Latest Version
.. image:: https://pypip.in/d/tekuila/badge.png
        :target: https://pypi.python.org/pypi/tekuila/
        :alt: Downloads
.. image:: https://pypip.in/license/tekuila/badge.png
        :target: https://pypi.python.org/pypi/tekuila/
        :alt: License

.. image:: https://travis-ci.org/mikeodr/tekuila.svg?branch=master
    :target: https://travis-ci.org/mikeodr/tekuila
    :alt: Build Status

Versions
--------

Works with python 2.6 - 3.4

Pull your TekSavvy Quota and act on it.

To avoid using command line flags create a config file at::

    ~/.tekuila

Place the following variables within the config file::

    API=<your API KEY from https://myaccount.teksavvy.com/ApiKey/ApiKeyManagement>
    CAP=<your cap in GB>
    WARN_RATIO=<ratio % to warn in 0.1 increments up to 1.0>

Installation
------------

To install, run the following::

    pip install tekuila

Or, if you wish to install the latest from source::

    git clone https://github.com/mikeodr/tekuila
    cd tekuila
    python setup.py install

API Usage
---------

`Readthedocs <http://tekuila.readthedocs.org/en/latest/>`_.

Console Usage
-------------

Console command help::

    tekuila -h
    usage: tekuila [-h] [-c CONFIG] [--cap CAP] [--API API] [--warn WARN] [-v]

    Check TekSavvy Cap

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Alternative config file
      --cap CAP             Your cap in GB
      --API API             API Key
      --warn WARN           Warn ratio against data cap, causes nonzero return
                            code
      -v, --verbose         Show output, don't just use return code

Pull Requests and Issues
------------------------

Pull requests very much welcome.
Check that it complies with pep8, please make sure the documentation builds.

Please use elementary commits vs big commits and try and have your commit
messages be detailed. See Tim Pope's excellent `guide
<http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.

License
-------
GPLv2
