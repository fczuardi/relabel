import os, sys

RELABEL_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(RELABEL_ROOT, 'lib'))

from fabric.api import *
import redis, base64

# from relabel import Relabel
  
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
  redis_pid_file = os.path.join(RELABEL_ROOT, 'run', 'redis.pid')
  redis_db_file = os.path.join(RELABEL_ROOT, 'data', 'relabel.rdb')
  redis_options = {
    'pidfile /var/run/redis.pid': 'pidfile %s' % redis_pid_file,
    'daemonize no': 'daemonize yes',
    'dbfilename dump.rdb': 'dbfilename %s' % redis_db_file
  }
  # read redis default configuration parameters
  redis_config = open(os.path.join(RELABEL_ROOT, 'ext', 'redis', 'redis.conf.orig'), 'r')
  redis_config_raw = redis_config.read()
  redis_config.close()
  # write redis app-specific configuration parameters
  redis_config_path = os.path.join(RELABEL_ROOT, 'ext', 'redis', 'redis.conf')
  redis_config = open(redis_config_path, 'w')
  for defaultv, newv in redis_options.items():
    redis_config_raw = redis_config_raw.replace(defaultv, newv)
  redis_config.write(redis_config_raw)
  redis_config.close()
  # start redis server
  local("%s %s" % (os.path.join(RELABEL_ROOT, 'ext', 'redis', 'redis-server'), redis_config_path))
  
def kill_redis():
  # kill redis server
  local("kill `cat %s`" % os.path.join(RELABEL_ROOT, 'run', 'redis.pid'))

def flush_redis(db=0):
  r = redis.Redis(host='localhost', port=6379)
  if type(db) is int: # flushes data from one specific DB
    r.select(r.host, r.port, db)
    r.flush()
  elif db is None: # flushes data from all DBs
    r.flushall()

class Relabel:
  @staticmethod
  def key(*args):
    return 'relabel:%s' % ':'.join(args)
  @staticmethod
  def settagnx(conn, tag):
    encoded_tag = base64.encodestring(tag).strip()
    tag_id_key = key('tag', encoded_tag, 'id')
    tag_id_in_db = conn.get(tag_id_key)
    if tag_id_in_db is None:
      next_tag_id = conn.incr(key('next', 'tag', 'id'))
      tag_id = conn.setnx(tag_id_key, next_tag_id)
      if tag_id:
        return tag_id
      else:
        return conn.get(tag_id_key)

def try_registering_a_tag():
  conn = redis.Redis(host='localhost', port=6379)
  Relabel.settagnx(conn, 'sample_tag')
  conn.disconnect()

def try_assoc_tag_to_item():
  conn = redis.Redis(host='localhost', port=6379)
  item_id = '1'
  # conn.setnx(tag('items', item_id, '
  conn.disconnect()
  
# sadd news:1000:tags 1
# sadd news:1000:tags 2
# sadd news:1000:tags 5
# sadd news:1000:tags 77
# sadd tag:1:objects 1000
# sadd tag:2:objects 1000
# sadd tag:5:objects 1000
# sadd tag:77:objects 1000
