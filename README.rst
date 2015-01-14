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

API Usage
=========

Documentation comming soon.

Console Usage
=============

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

License
=======
GPLv2
