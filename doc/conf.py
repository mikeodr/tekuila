# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon'
]

autoclass_content = 'both'

source_suffix = '.rst'

master_doc = 'index'

project = u'tekuila'
copyright = u'2015, Mike O\'Driscoll'

from tekuila import __version__
version = __version__
release = version

language = 'en'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

html_theme = 'default'

man_pages = [
    ('index', 'tekuila', u'tekuila Documentation',
     [u'Mike O\'Driscoll'], 1)
]

texinfo_documents = [
  ('index', 'tekuila', u'tekuila Documentation',
   u'Mike O\'Driscoll', 'tekuila', 'API and console command for accessing your ISP quotas.',
   'Miscellaneous'),
]
