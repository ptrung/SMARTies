#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/smarties")

from app import app as application
application.secret_key = 'i_am_a_super_secrete_key'
