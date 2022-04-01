import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BUNDLE_ERRORS = True
    PRODUCT_LOCATION = "PATH" # Where the raster data is located
