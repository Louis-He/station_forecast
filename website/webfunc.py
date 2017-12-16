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

def iscookie():
    access = web.cookies().get('access')
    if access:
        return True
    else:
        return False

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
            web.setcookie('access', i.access, 30)
            return 'Login Success'
        else:
            return 'Login Error\n Please check your username and password'

class CookieSet:
    def GET(self):
        i = web.input(access='True')
        web.setcookie('access', i.access, 5)
        return "ACCESS set in your cookie"

class CookieGet:
    def GET(self):
        if iscookie():
            return "Logged in"
        else:
            return open(r'login.html', 'r').read()

if __name__ == "__main__":
    app.run()
