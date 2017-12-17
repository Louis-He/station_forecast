import web
urls = (
    '/index', 'index',
    '/login', 'login',
    '/logout', 'logout',
    '/logerror', 'logerror',
    '/missionlist', 'missionlist',
    '/product', 'product',
    '/addmission', 'addmission',
    '/setcookie', 'CookieSet',
    '/getcookie', 'CookieGet'
)
app = web.application(urls, globals())

allowed = (
	('admin','admin'),
)

def iscookie():
    access = web.cookies().get('access')
    if access=='True':
        return True
    else:
        return False

class index:
    def GET(self):
        if iscookie():
            return open(r'index.html', 'r').read()
        else:
            return open(r'login.html', 'r').read()

class login:
    def GET(self):
        return open(r'login.html', 'r').read()

    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('passwd')
        if (username, passwd) in allowed:
            i = web.input(access='True')
            web.setcookie('access', i.access, 180)
            return open(r'index.html', 'r').read()
        else:
            return open(r'logerror.html', 'r').read()

class logerror:
    def GET(self):
        return open(r'logerror.html', 'r').read()

class logout:
    def GET(self):
        i = web.input(access='False')
        web.setcookie('access', i.access, 60)
        return open(r'logout.html', 'r').read()

class missionlist:
    def GET(self):
        if iscookie():
            return open(r'missionlist.html', 'r').read()
        else:
            return open(r'login.html', 'r').read()

class product:
    def GET(self):
        if iscookie():
            return open(r'product.html', 'r').read()
        else:
            return open(r'login.html', 'r').read()

class addmission:
    def GET(self):
        if iscookie():
            return open(r'addmission.html', 'r').read()
        else:
            return open(r'login.html', 'r').read()

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

