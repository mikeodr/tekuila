# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname("../")))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode'
]

autoclass_content = 'both'

source_suffix = '.rst'

master_doc = 'index'

project = u'tekuila'
copyright = u'2015, Mike O\'Driscoll'

version = '2.0.2'
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
   u'Mike O\'Driscoll', 'tekuila', 'One line description of project.',
   'Miscellaneous'),
]
