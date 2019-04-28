# pylint: skip-file
"""
Import submodule __all__ members so that they can be accessed directly through main package import.

This creates an import pattern where all "public" methods will be available through import of main package
so that downstream consumers do not have any dependencies on internal structure of this package. Of course
all methods are importable/public but if objects are not available through base import (i.e. import simple_app)
they should be treated as "private" and they can be moved within the package potentially breaking downstream imports.
"""
from simple_app import app
from simple_app import errors


from simple_app.app import *
from simple_app.errors import *


__all__ = (
    list(app.__all__)
    + list(errors.__all__)
)


import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Avoid 'no handlers could be found for logger' warnings if logging not configured for application
logging.getLogger(__name__).addHandler(NullHandler())


__author__ = 'Matt Kracht'
__email__ = 'mwkracht@gmail.com'
__license__ = 'MIT'
__version__ = '0.0.1'
