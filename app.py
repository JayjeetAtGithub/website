from api import API
from models import HttpResponse

app = API(__name__, 1.0)
app2 = API(__name__,1.0)

# def check(req):
#     return app.redirect(req, "/red")


def red(req):
    response = HttpResponse("Working 200")
    response.mimetype = "text/html"
    return response

def welcome(req):
    print(req.method)
    template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Welcome to MINI 1.0</title>
            <style>
                body{
                    text-align:center;
                }
                h1{
                    color : blue;
                }
            </style>
        </head>
        <body>
            <h1> This is your first Mini powered page </h1>
        </body>
    </html>
    """
    response = HttpResponse(template)
    response.mimetype = "text/html"
    response.status = "200 OK"
    response.update_headers("X-Auth","67bd6bd7")
    return response


# app.add_route("/check", check)
# app.add_route("/red", red)
app.add_route("/", welcome)
app2.add_route("/",red)
app2.add_route("welcome/",welcome)
app.mount_wsgi_app("app2/",app2)

# print(app.get_static_url('script.ts'))
# app.run('',9000)



