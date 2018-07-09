#!/usr/bin/python

import cantools

from pprint import pprint

dbc = cantools.db.load_file('../dbc/ford_fusion_2018.dbc')
print dbc.messages