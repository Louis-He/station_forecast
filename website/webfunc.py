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
    '/success', 'success',
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
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            return open(r'index.html', 'r').read()
        else:
            return web.redirect('login')


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
            web.setcookie('access', i.access, 600)
            return open(r'index.html', 'r').read()
        else:
            return web.redirect('logerror')

class logerror:
    def GET(self):
        return open(r'logerror.html', 'r').read()

class logout:
    def GET(self):
        i = web.input(access='False')
        web.setcookie('access', i.access, 600)
        return open(r'logout.html', 'r').read()

class missionlist:
    def GET(self):
        result = ''
        count = 1

        f = open('waitlistmission.sh')  # Read waitlist mission
        tmp = ''
        line = f.readline()
        while line:
            tmp = line
            tmp = tmp.replace('\n', '')
            while (tmp.find(' ') != -1):
                py = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                process = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                _lon = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                lon = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                _lat = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                lat = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                _source = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                source = tmp[0:len(tmp)]

                result+='<tr><td>' + str(count) + '</td><td>' + source + '</td><td>' + lon + '</td><td>' + lat + '</td></tr>'

            count += 1
            line = f.readline()
        f.close()

        if iscookie() == True:
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            return open(r'missionlisthead.html', 'r').read() + result + open(r'missionlistbottom.html', 'r').read()
        else:
            return web.redirect('login')

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

                model = file[0:file.find('_')]
                file = file[file.find('_'):]
                if file.find('E') != -1:
                    lon = file[1:file.find('E') + 1]

                    if file.find('N') != -1:
                        lat = file[file.find('E') + 1:file.find('N') + 1]
                    else:
                        lat = file[file.find('E') + 1:file.find('S') + 1]
                else:
                    lon = file[1:file.find('W') + 1]

                    if file.find('N') != -1:
                        lat = file[file.find('W') + 1:file.find('N') + 1]
                    else:
                        lat = file[file.find('W') + 1:file.find('S') + 1]

                result += '<p>时序图（模式：' + model + '  坐标：'+ lon + ',' + lat +'）</p>'
                result += '</div></div></div><div class="overlay"></div></div></div></div></div><!-- col-lg-4 -->'

                if colcount == 2:
                    result += '</div><!-- /row -->'
                colcount += 1

        if iscookie()==True:
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            #print(open(r'product.html', 'r').read())
            return open(r'producthead.html', 'r').read() + result + open(r'productbottom.html', 'r').read()
        else:
            return web.redirect('login')

class addmission:
    def GET(self):
        i = web.input()
        print(i)

        try:
            lon = i.get('lon')
            lat = i.get('lat')
            source = i.get('optionsRadios')
            print('!![LON]!!' + lon)
            print('!![LAT]!!' + lat)
            print('!![SOURCE]!!' + source)
            read = True
            f = open('waitlistmission.sh', 'a+')
            f.write('python3 main.py --lon ' + lon + ' --lat '+ lat +' --source ' + source + '\n')
            print('!![PRCOESS]!!')
            f.close()

            return web.redirect('success')
        except:
            print('ERROR')

        if iscookie()==True:
            return open(r'addmission.html', 'r').read()
        else:
            return web.redirect('login')

class success:
    def GET(self):
        if iscookie() == True:
            return open(r'success.html', 'r').read()
        else:
            return web.redirect('login')

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
    f = open('waitlistmission.sh', 'w+')
    f.close()
    app.run()

