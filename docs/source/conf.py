# -*- coding: utf-8 -*-
import sys, os
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'OpenStack Security Advisories'
copyright = u'2014, Grant Murphy'
version = '0.1'
release = '0.1'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
html_show_copyright=False
html_show_sphinx=False
# local override rtd theme
if not os.environ.get('READTHEDOCS', None) == 'True':
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']
htmlhelp_basename = 'OpenStackSecurityAdvisoriesdoc'
