TekSavvyQuota
=============

Pull your TekSavvy Quota and act on it.

To avoid using command line flags create a config file at
`~/.tekquota`

Place the following variables within the config file:
```bash
API=<your API KEY from https://myaccount.teksavvy.com/ApiKey/ApiKeyManagement>
CAP=<your cap in GB>
WARN_RATIO=<ratio % to warn in 0.1 increments up to 1.0>
```
