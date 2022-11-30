#!/usr/bin/env python3

import logging
from src import CustomLogger as cl

###>> Configure logger
logger = cl.CustomLogger('drac')
logger.propagate = False
