import os, sys
RELABEL_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(RELABEL_ROOT, 'lib'))

from relabel import Relabel
  
def web():  
  http_server = tornado.httpserver.HTTPServer(Relabel.application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
  
def start_redis():
  # setup directories (should probably go under version control later)
  if not os.path.exists(os.path.join(RELABEL_ROOT, 'run')):
    os.makedirs(os.path.join(RELABEL_ROOT, 'run'))
  if not os.path.exists(os.path.join(RELABEL_ROOT, 'data')):
    os.makedirs(os.path.join(RELABEL_ROOT, 'data'))
    
  # define redis configuration parameters
  redis_pid_file = os.path(RELABEL_ROOT, 'run', 'redis.pid')
  redis_db_file = os.path.join(RELABEL_ROOT, 'data', 'relabel.rdb')
  redis_options = {
    'pidfile /var/run/redis.pid': 'pidfile %s' % redis_pid_file,
    'daemonize no': 'daemonize yes',
    'dbfilename dump.rdb': 'dbfilename %s' % redis_db_file
  }

  # write redis configuration parameters
  redis_config = open(os.path.join(RELABEL_ROOT, 'ext', 'redis', 'redis.conf'), 'w')
  redis_config_raw = redis_config.read()
  redis_config.close()
  redis_config = open(os.path.join(RELABEL_ROOT, 'ext', 'redis', 'redis.conf'), 'w')
  for defaultv, newv in redis_options.items():
    redis_config_raw = redis_config_raw.replace(defaultv, newv)
  redis_config.write(redis_config_raw)
  redis_config.close()

  # start redis server
  local(os.path(RELABEL_ROOT, 'ext', 'redis-server'))
  
def kill_redis():
  # start redis server
  local("kill `cat %s`" % os.path(RELABEL_ROOT, 'run', 'redis.pid'))
