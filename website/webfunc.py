import web
urls = (
    '/index', 'index',
    '/setcookie', 'CookieSet',
    '/getcookie', 'CookieGet'
)
app = web.application(urls, globals())

class index:
    def GET(self):
        return "index Page."

class CookieSet:
    def GET(self):
        i = web.input(access='True')
        web.setcookie('access', i.access, 3600)
        return "ACCESS set in your cookie"

class CookieGet:
    def GET(self):
        age=web.cookies().get('access')
        if age:
            return "Your age is: %s" % age
        else:
            return "Cookie does not exist."

if __name__ == "__main__":
    app.run()

