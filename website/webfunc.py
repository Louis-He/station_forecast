import web
import os
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
        if iscookie()==True:
            return open(r'index.html', 'r').read()
        else:
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

class login:
    def GET(self):
        if iscookie()==True:
            return open(r'index.html', 'r').read()
        else:
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
        if iscookie() == True:
            return open(r'missionlist.html', 'r').read()
        else:
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

class product:
    def GET(self):
        path = 'static/images/'
        files = os.listdir(path)
        piclist = [];
        colcount = 0
        rowcount = 0
        result = ''
        for file in files:
            if file[-3:] == 'png':
                if colcount == 0:
                    result += '<div class="row mt">'

                result += '<div class="col-lg-4 col-md-4 col-sm-4 col-xs-12 desc"><div class="project-wrapper"><div class="project"><div class="photo-wrapper"><div class="photo">'
                result += '<a class="fancybox" href="static/images/'+file+'"><img class="img-responsive" src="static/images/'+file+'" alt=""></a>'
                result += '<div class="row mt"><div class="col-lg-12">'
                file = file[file.find('_'):]
                if file.find('E') != -1:
                    lon = file[0:file.find('E') + 1]
                else:
                    lon = file[0:file.find('W') + 1]

                if file.find('N') != -1:
                    lat = file[0:file.find('N') + 1]
                else:
                    lat = file[0:file.find('S') + 1]

                result += '<p>时序图（坐标：'+ lon + ',' + lat +'）</p>'
                result += '</div></div></div><div class="overlay"></div></div></div></div></div><!-- col-lg-4 -->'

                if colcount == 2:
                    result += '</div><!-- /row -->'
                colcount += 1

        if iscookie()==True:
            #print(open(r'product.html', 'r').read())
            return open(r'producthead.html', 'r').read() + result + open(r'productbuttom.html', 'r').read()
        else:
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

class addmission:
    def GET(self):
        if iscookie()==True:
            return open(r'addmission.html', 'r').read()
        else:
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

