import atexit

from MySQLdb import *

import config


#db = connect(**config.config['mysql'])
#atexit.register(db.close)
db = None
