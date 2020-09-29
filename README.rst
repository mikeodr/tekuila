tekuila
=============

Interface for querying your ISP download quota.

"Have you had to much to download?"

|travis| |version| |ghversion| |license|

Versions
--------

Works with python 2.7, 3.4, 3.5

Pull your ISP Quota and act on it.

Supported ISPs:

- `TekSavvy`_ **This has been deprecated** See `Deprecated`_
- `Start.ca`_

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
    usage: tekuila [-h] [-c CONFIG] [--cap CAP] [--api API] [--warn WARN] [-v]
                   [-s] [--version]

    Check TekSavvy Cap

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Alternative config file
      --cap CAP             Your cap in GB, causes nonzero return code if exceeded
      --api API             API Key
      --warn WARN           Warn ratio against data cap, causes nonzero return
                            code if exceeded, in range 0.1 to 1.0
      -v, --verbose         Show output, don't just use return code
      -s, --startca         Use StartCA instead of TekSavvy API
      --version             show program's version number and exit

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
.. _TekSavvy: https://teksavvy.com/
.. _Start.ca: https://www.start.ca/
.. _Deprecated: https://community.teksavvy.com/discussion/comment/120#Comment_120

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
