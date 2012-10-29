# -*- coding: utf-8 -*-
import web

__author__    = "Jorge Alonso Toro (jolth) [jolthgs@gmail.com]"
__version__   = "0.1.3"
__date__      = "28 feb 2012"
__copyright__ = "Copyright (c) 2012 Jorge A. Toro"
__license__   = "BSD"

DB = web.database(dbn='postgres', user='postgres', pw='qwerty', db='cowfleet')

transaction = DB.transaction()
cache = False
