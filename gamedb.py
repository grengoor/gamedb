import atexit

import pymysql

from mysql_config import config


db = pymysql.connect(**config['mysql'])
atexit.register(db.close)
