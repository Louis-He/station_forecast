import web
urls = (
    '/index', 'index',
    '/login', 'login',
    '/setcookie', 'CookieSet',
    '/getcookie', 'CookieGet'
)
app = web.application(urls, globals())

allowed = (
	('admin','admin'),
)

class index:
    def GET(self):
        return "index Page."

class login:
    def GET(self):
        return open(r'login.html', 'r').read()

    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('passwd')
        if (username, passwd) in allowed:
            i = web.input(access='True')
            web.setcookie('access', i.access, 5)
            return 'Login Success'
        else:
            return '<h1>Login Error!!!</h1></br><a href="/login">Login</a>'

class CookieSet:
    def GET(self):
        i = web.input(access='True')
        web.setcookie('access', i.access, 5)
        return "ACCESS set in your cookie"

class CookieGet:
    def GET(self):
        access = web.cookies().get('access')
        if access:
            return "Your Access status is: %s" % access
        else:
            return "Cookie does not exist."

if __name__ == "__main__":
    app.run()

