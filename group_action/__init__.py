"""
Group Action Package

This package provides tools for handling group actions.
"""

__version__ = "0.1.8"

from os import cpu_count
__num_of_cores__ = cpu_count()

# from .module1 import MyClass
# from .module2 import my_function

# __all__ = ['MyClass', 'my_function']

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Package group_action initialized")
