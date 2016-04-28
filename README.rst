tekuila
=============

Interface for querying your ISP download quota.

"Have you had to much to download?"

|travis| |version| |ghversion| |pypidownloads| |landscape| |license|

Versions
--------

Works with python 2.6 - 3.4

Pull your ISP Quota and act on it.

Supported ISPs:

- TekSavvy
- Start.ca

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

`ReadTheDocs`_.

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
      -s, --startca         Use StartCA instead of TekSavvy API

Pull Requests and Issues
------------------------

Pull requests very much welcome.
Check that it complies with pep8, please make sure the documentation builds.

Please use elementary commits vs big commits and try and have your commit
messages be detailed. See Tim Pope's excellent `Guide`_.

License
-------
GPLv2

.. _Guide: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
.. _ReadTheDocs: http://tekuila.readthedocs.io/en/latest/

.. |travis| image:: https://img.shields.io/travis/mikeodr/tekuila.svg
        :target: https://travis-ci.org/mikeodr/tekuila
        :alt: Build Status

.. |license| image:: https://img.shields.io/pypi/l/tekuila.svg
        :target: https://pypi.python.org/pypi/tekuila/
        :alt: License

.. |version| image:: https://img.shields.io/pypi/v/tekuila.png
        :target: https://pypi.python.org/pypi/tekuila/
        :alt: Latest Version released on PyPi

.. |ghversion| image:: https://img.shields.io/github/release/mikeodr/tekuila.svg
        :target: https://github.com/mikeodr/tekuila/releases
        :alt: Latest Version released on Github

.. |pypidownloads| image:: https://img.shields.io/pypi/dm/tekuila.png
        :target: https://pypi.python.org/pypi/tekuila/
        :alt: Downloads on Pypi

.. |landscape| image:: https://landscape.io/github/mikeodr/tekuila/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mikeodr/tekuila/master
   :alt: Code Health
