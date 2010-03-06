import tornado.httpserver
import tornado.ioloop
import tornado.web

# $app_prefix:tags

# sadd news:1000:tags 1
# sadd news:1000:tags 2
# sadd news:1000:tags 5
# sadd news:1000:tags 77
# sadd tag:1:objects 1000
# sadd tag:2:objects 1000
# sadd tag:5:objects 1000
# sadd tag:77:objects 1000


# By using 
# SETNX if a different client was faster than this one the key wil not be 
# setted. Not only, SETNX returns 1 if the key is set, 0 otherwise. So...
# let's add a final step to our computation. If SETNX returned 1 (We set
#  the key) return 123456 to the caller, it's our tag ID, otherwise perform
#  GET tag:b840fc02d524045429941cc15f59e41cb7be6c52:id and return the value
# to the caller.

# $app_prefix:tags
# $app_prefix:items
# $app_prefix:authors

# $app_prefix:tag:$tag
# $app_prefix:item:$item
# $app_prefix:author:$author

# $app_prefix:tag:$tag:authors
# $app_prefix:tag:$tag:items
# $app_prefix:tag:$tag:authors:total
# $app_prefix:tag:$tag:items:total

# $app_prefix:item:$item:tags
# $app_prefix:item:$item:authors
# $app_prefix:item:$item:tags:total
# $app_prefix:item:$item:authors:total

# $app_prefix:author:$author:tags
# $app_prefix:author:$author:items
# $app_prefix:author:$author:tags:total
# $app_prefix:author:$author:items:total

# >>> import redis
# >>> r = redis.Redis(host='localhost', port=6379, db=0)
# >>> r.set('foo', 'bar')   # or r['foo'] = 'bar'
# True
# >>> r.get('foo')
# 'bar'

class Relabel:
  
  class Tag(tornado.web.RequestHandler):
    def post(self):
      # POST {@tag, @author, @item} to /tags => 200 Ok


    def delete(self):
      # DELETE /tags/%tag?item=%item => 200 Ok
      # DELETE /tags/%tag?item=%item&author=%author => 200 Ok


  class Item(tornado.web.RequestHandler):
    def get(self):
      # GET /items/%item/tags => 200 Ok, ['tag', 'tag', 'tag']
      # GET /items/%item/tags/%tag/authors => 200 Ok, ['jonasgalvez@gmail.com' ... ]

  
  class Author(tornado.web.RequestHandler):
    def post(self):
      # POST {tag: 'foo'} to /items/%item/tags => 200 Ok


  application = application = tornado.web.Application([
    (r"/tags*", Tag),
    (r"/items*", Item),
    (r"/authors*", Author)
  ])
