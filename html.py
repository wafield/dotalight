import os.path

__ASSET_LOCATION = 'html/'

__ASSET_LOCATION = os.path.join(os.path.dirname(__file__), __ASSET_LOCATION)

HTML = {}

# ===============================
# Register asset after this line

HTML['portal'] = 'portal.html'

# Register asset before this line
# ===============================

for key, value in HTML.items():
    asset = open(os.path.join(__ASSET_LOCATION, value), 'r')
    HTML[key] = asset.read()
    asset.close()
