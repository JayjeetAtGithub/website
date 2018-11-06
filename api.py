from models import HttpRequest, HttpResponse
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server


class Route:

    def __init__(self, path, endpoint, *args, **kwargs):
        self.path = path
        self.endpoint = endpoint

    def execute(self, req):
        if callable(self.endpoint):
            return self.endpoint(req)


class API:

    def __init__(self, name, version, *args, **kwargs):
        self.name = name
        self.version = version
        self.routes = {}
        self.static_route = "/static"
        self.media_route = "/media"
        self.template_route = "/templates"
        self.apps = {}

    def add_route(self, path, endpoint):
        """Adds new routes"""
        self.routes[path] = Route(path, endpoint)

    def get_static_url(self, asset):
        return "%s/%s" % (self.static_route, str(asset))

    def mount_wsgi_app(self, path, app):
        """Add new app to route"""
        self.apps[path] = app

    def redirect(self, req, path):
        response = HttpResponse()
        response.status = "301 MOVED_PERMANENTLY"
        response.update_headers("Location", path)
        return response

    def validate_route_and_call_endpoint(self, path):
        """Validates the routes and executes them"""
        if path in self.routes:
            route = self.routes[path]
            if callable(route.endpoint):
                return route.execute(self.request)
            else:
                raise ValueError('A callable was expected')
        elif path in self.apps:
            app = self.apps[path]
            app()
        else:
            res_404 = HttpResponse("404 Not Found")
            res_404.status = "404 NOT_FOUND"
            return res_404

    def shift_path(self, level, path):
        """Shifts the path by level amount deeper"""
        path_list = path.split("/")
        path_list = path_list[level+1:]
        temp_list = []
        for p in path_list:
            if p != " ":
                temp_list.append(p)

        new_path = "/"
        for p in temp_list:
            new_path = new_path + ("%s/" % p)
        return new_path[1:]

    def get_base_mount_path(self, path):
        """Returns the base mount path of the app"""
        path_list = path.split("/")
        path_list = path_list[1:2]
        temp_list = []
        for p in path_list:
            if p != " ":
                temp_list.append(p)

        new_path = "/"
        for p in temp_list:
            new_path = new_path + ("%s/" % p)
        return new_path[1:]

    def wsgi(self, environ, start_reponse):
        """The main WSGI application callable"""
        response = self.validate_route_and_call_endpoint(self.request.path)
        headers = []
        for k, v in response.headers.items():
            headers.append((k, v))
        start_reponse(response.status, headers)
        return iter([response.content])

    def __call__(self, environ, start_response):
        """For running the server by calling the application callable"""
        self.request = HttpRequest(environ)
        # print("__call__ was called for %s" % self.request.path)
        if self.get_base_mount_path(self.request.path) in self.routes:
            return self.wsgi(environ, start_response)
        elif self.get_base_mount_path(self.request.path) in self.apps:
            app = self.apps[self.get_base_mount_path(self.request.path)]
            environ_cp = environ
            environ_cp['PATH_INFO'] = self.shift_path(1, self.request.path)
            return app(environ_cp, start_response)

    def wsgi_app_caller(self, environ, start_response):
        self.request = HttpRequest(environ)
        return self.wsgi(environ, start_response)

    def run(self, host, port):
        """Run the app on a local development server"""
        server = make_server(host, port, self.wsgi_app_caller,
                             WSGIServer, WSGIRequestHandler)
        try:
            print("Listening on port %s" % port)
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()


