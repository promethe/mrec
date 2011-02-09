#!/usr/bin/env python
#
# kakapo
# ------
# this file contains the kakapo setup for paths, ids, etc.
#
# (c) bogo giertler in '11

import sys
import logging

# PATH extensions
sys.path.append("extern/facebook-python-sdk/src")

# Fb setup
FACEBOOK_APP_ID = "184419424921829"
FACEBOOK_APP_SECRET = "fb60740cc8f8fa7173f15470651770fd"

# varia
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
