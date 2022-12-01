#!/usr/bin/env python3

###>> Configure version info
from .__version__ import __version__

###>> Configure logger
from .CustomLogger import CustomLogger
logger = CustomLogger('budi')
logger.propagate = False
