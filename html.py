import os.path
import jinja2

__ASSET_LOCATION = 'html/'

__ASSET_LOCATION = os.path.join(os.path.dirname(__file__), __ASSET_LOCATION)

HTML = {}

# ===============================
# Register asset after this line

HTML['portal'] = 'portal.html'
HTML['dashboard'] = 'dashboard.html'
HTML['match_table'] = 'match_table.html'
HTML['error'] = 'error.html'

# Register asset before this line
# ===============================

for key, value in HTML.items():
    asset = open(os.path.join(__ASSET_LOCATION, value), 'r')
    HTML[key] = asset.read()
    asset.close()

# =============================================
# If the asset is a template, construct it here
HTML['dashboard'] = jinja2.Template(HTML['dashboard'])
HTML['match_table'] = jinja2.Template(HTML['match_table'])
HTML['error'] = jinja2.Template(HTML['error'])

