import atexit

import pymysql

import config


db = pymysql.connect(**config.config['mysql'])
atexit.register(db.close)
db = None
