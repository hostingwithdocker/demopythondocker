import falcon
from config import cfg


class HelloResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = ('Hello World from %s' % cfg('app', 'name'))


app = falcon.API()
greeting = HelloResource()
app.add_route('/', greeting)
