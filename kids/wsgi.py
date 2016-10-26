#
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2013 IBM Corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Utility methods for working with WSGI servers."""

import os
import signal
import sys
import time

import eventlet
from oslo_log import log as logging
from oslo_service import service
from paste import deploy
import routes
import routes.middleware
import six
import webob
import webob.dec
import webob.exc


LOG = logging.getLogger(__name__)

class Server(service.ServiceBase):
    """Server class to manage a WSGI server, serving a WSGI application."""

    def __init__(self):
        pass
    def start(self):
        """Start serving a WSGI application.
        """
        pass

    def stop(self):
        pass

    def wait(self):
        pass


class Request(webob.Request):

    def __init__(self):
        pass


class Middleware(object):

    def __init__(self,application):
        self.application=application

    @webob.dec.wsgify
    def __call__(self,req):
        pass


class Debug(Middleware):
    """Helper class to get information about the request and response.

    Helper class that can be inserted into any WSGI application chain
    to get information about the request and response.
    """

    @webob.dec.wsgify
    def __call__(self,req):
        print(("*" * 40) + " REQUEST ENVIRON")
        for key, value in req.environ.items():
            print(key, "=", value)
        print()
        resp = req.get_response(self.application)

        print(("*" * 40) + " RESPONSE HEADERS")
        for (key,value) in six.iteritems(resp.headers):
            print(key, "=", value)
        print()

        resp.app_iter = self.print_generator(resp.app_iter)

        return resp

    @staticmethod
    def print_generator(app_iter):
        """Iterator that prints the contents of a wrapper string."""
        print(("*" * 40) + " BODY")
        for part in app_iter:
            sys.stdout.write(part)
            sys.stdout.flush()
            yield part
        print()


class Router(object):
    """WSGI middleware that maps incoming requests to WSGI apps."""

    def __init__(self, mapper):
        """Create a router for the given routes.Mapper.

        Each route in `mapper` must specify a 'controller', which is a
        WSGI app to call.  You'll probably want to specify an 'action' as
        well and have your controller be an object that can route
        the request to the action-specific method.

        Examples:
          mapper = routes.Mapper()
          sc = ServerController()

          # Explicit mapping of one route to a controller+action
          mapper.connect(None, '/svrlist', controller=sc, action='list')

          # Actions are all implicitly defined
          mapper.resource('server', 'servers', controller=sc)

          # Pointing to an arbitrary WSGI app.  You can specify the
          # {path_info:.*} parameter so the target app can be handed just that
          # section of the URL.
          mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())

        """
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.map)

    @webob.dec.wsgify
    def __call__(self,req):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.

        """
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        """Dispatch the request to the appropriate controller,
        Returns controller after matching the incoming request to a route.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app


class Loader(object):
    """Used to load WSGI applications from paste confiturations."""

    def __init__(self,config_path=None):
        """Initialize the loader, and attempt to find the config.

        :param config_path: Full or relative path to the paste config.
        :returns: None

        """
        self.config_path = None

        config_path = config_path or CONF.wsgi.api_paste_config
        # CONF = nova.conf.CONF

        


    def load_app(self,name):
        """Return the paste URLMap wrapped WSGI application.

        :param name: Name of the application to load.
        :returns: Paste URLMap object wrapping the requested application.
        :raises: `nova.exception.PasteAppNotFound`

        """
        try:
            return deploy.loadapp("config:%s" % self.)
