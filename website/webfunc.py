import web
import os
urls = (
    '/index', 'index',
    '/login', 'login',
    '/logout', 'logout',
    '/logerror', 'logerror',
    '/missionlist', 'missionlist',
    '/product', 'product',
    '/addmapmission', 'addmapmission',
    '/addmission', 'addmission',
    '/success', 'success',
    '/GFSrain', 'GFSrain',
    '/GFSsurf', 'GFSsurf',
    '/GFS500', 'GFS500',
    '/updatehistory', 'updatehistory',
    '/setcookie', 'CookieSet',
    '/getcookie', 'CookieGet'
)
app = web.application(urls, globals())

allowed = (
    ('qxahz','Tybbs'),# Forever
    ('user02','123roxc8'),# ~2017.02.02
    ('user03','wo8cnqw7'),# ~2017.02.03
    ('user04','1huxe271'),# ~2017.02.03
    ('user05','sd7ar9d2'),# ~2017.06.03
    ('user06','sa675scz'),# ~2017.02.03
    ('user07','a8sd979a'),# ~2017.02.05
    ('user08','sd8f7sf9'),# ~2017.02.05
    ('user09','asd7bc9v')#~2017.02.07
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
            return web.redirect('index')
        else:
            return open(r'login.html', 'r').read()

    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('passwd')
        if (username, passwd) in allowed:
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            i = web.input(user=username)
            web.setcookie('user', i.user, 600)
            return web.redirect('index')
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

                source = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                _type = tmp[0:tmp.find(' ')]
                tmp = tmp[tmp.find(' ') + 1:len(tmp)]

                type = tmp[0:len(tmp)]


                result+='<tr><td>' + str(count) + '</td><td>' + type + '</td><td>' + source + '</td><td>' + lon + '</td><td>' + lat + '</td></tr>'

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

                type = file[0:file.find('_')]
                file = file[file.find('_') + 1:]

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
                if type == 'V':
                    result += '<p>垂直剖面时序图（模式：' + model + '  坐标：'+ lon + ',' + lat +'）</p>'
                elif type == 'G':
                    result += '<p>地面要素时序图（模式：' + model + '  坐标：' + lon + ',' + lat + '）</p>'
                elif type == 'A':
                    result += '<p>灾害天气风险预报图（模式：' + model + '  坐标：' + lon + ',' + lat + '）</p>'
                elif type == 'M':
                    result += '<p>区域天气要素预报图（模式：GFS  区域）</p>'
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
        print('PROCESS GET method')
        if iscookie()==True:
            return open(r'addmission.html', 'r').read()
        else:
            return web.redirect('login')

    def POST(self):
        print('PROCESS POST method')
        try:
            print(web.input())
        except:
            print('web input ERROR!!!!')
        i = web.input()

        try:
            lon = i.get('lon')
            lat = i.get('lat')
            source = i.get('optionsRadios')
            plottype = i.get('plottype')
            print('!![LON]!!' + lon)
            print('!![LAT]!!' + lat)
            print('!![SOURCE]!!' + source)
            print('!![PLOT_TYPE]!!' + plottype)
            f = open('waitlistmission.sh', 'a+')
            f.write('python3 main.py --lon ' + lon + ' --lat ' + lat + ' --source ' + source + ' --type ' + plottype + '\n')
            print('!![PRCOESS]!!')
            f.close()
            return web.redirect('success')
        except:
            print('ERROR')

class addmapmission:
    def GET(self):
        print('PROCESS GET method')
        path = '/root/GFS/rawfile'
        files = os.listdir(path)
        piclist = [];
        colcount = 0
        rowcount = 0
        result = ''

        downloadhour = ['000', '006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072',
                        '078', '084',
                        '090', '096', '102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162',
                        '168', '174',
                        '180', '186', '192', '198', '204', '210', '216', '222', '228', '234', '240']

        count = 0

        finalfilelist = []
        for count in range(0, len(downloadhour)):
            for file in files:
                # gfs.GFS2017121718.f120
                fcst = file[file.find('.') + file[file.find('.') + 1:].find('.') + 3:]
                # print(fcst)

                if fcst == downloadhour[count]:
                    finalfilelist.append(file)

        for file in finalfilelist:
                result += '<option value="' + file + '"> ' + file + ' </option>'

        if iscookie()==True:
            rawhtml = open(r'addmapmission.html', 'r').read()
            return rawhtml[0:rawhtml.find('<select name="time" class="form-control">')+len('<select name="time" class="form-control">')] \
                   + result + rawhtml[rawhtml.find('<select name="time" class="form-control"></select>')+len('<select name="time" class="form-control">'):]
        else:
            return web.redirect('login')

    def POST(self):
        print('PROCESS POST method')
        try:
            print(web.input())
        except:
            print('web input ERROR!!!!')
        i = web.input()

        try:
            area = i.get('area')
            time = i.get('time')
            contourf = i.get('contourf')
            contourfcolor = i.get('contourfcolor')
            f = open('waitlistmission.sh', 'a+')
            f.write('python3 main.py --time ' + time + ' --type map --contourf ' + contourf + ' --contourfcolor ' + contourfcolor + ' --contour a --barb a --contourcolor a --area ' + area)
            print('!![PRCOESS]!!')
            f.close()
            return web.redirect('success')
        except:
            print('ERROR')

class GFSrain:
    def GET(self):
        path = 'static/images/model/GFS/RAIN'
        files = os.listdir(path)
        piclist = [];
        colcount = 0
        rowcount = 0
        result = ''

        downloadhour = ['000', '006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072',
                        '078', '084',
                        '090', '096', '102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162',
                        '168', '174',
                        '180', '186', '192', '198', '204', '210', '216', '222', '228', '234', '240']

        count = 0

        finalfilelist = []
        for count in range(0, len(downloadhour)):
            for file in files:
                #CNgfs.GFS2017121718.f120.png
                fcst = file[file.find('.') + file[file.find('.')+1:].find('.') + 3 : file.find('.png') ]
                #print(fcst)

                if fcst == downloadhour[count]:
                    finalfilelist.append(file)

        for file in finalfilelist:
            if file[-3:] == 'png':
                if colcount == 0:
                    result += '<div class="row mt">'

                result += '<div class="col-lg-4 col-md-4 col-sm-4 col-xs-12 desc"><div class="project-wrapper"><div class="project"><div class="photo-wrapper"><div class="photo">'
                result += '<a class="fancybox" href="static/images/model/GFS/RAIN/'+file+'"><img class="img-responsive" src="static/images/model/GFS/RAIN/'+file+'" alt=""></a>'
                result += '<div class="row mt"><div class="col-lg-12">'

                file = file[file.find('.')+1:]
                #year = file[file.find('GFS') + 3: file.find('GFS') + 7]
                month = file[file.find('GFS') + 7: file.find('GFS') + 9]
                day = file[file.find('GFS') + 9: file.find('GFS') + 11]
                hour = file[file.find('GFS') + 11: file.find('GFS') + 13]

                file = file[file.find('.') + 1:]
                fch = file[file.find('f') + 1: file.find('.')]

                result += '<p>降水（起报：' + month+'/'+day+'/'+hour + 'z  时效：' + fch +'）</p>'
                result += '</div></div></div><div class="overlay"></div></div></div></div></div><!-- col-lg-4 -->'

                if colcount == 2:
                    result += '</div><!-- /row -->'
                colcount += 1

        if iscookie()==True:
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            #print(open(r'product.html', 'r').read())
            return open(r'GFSrainhead.html', 'r').read() + result + open(r'GFSrainbottom.html', 'r').read()
        else:
            return web.redirect('login')

class GFSsurf:
    def GET(self):
        path = 'static/images/model/GFS/WTP'
        files = os.listdir(path)
        piclist = [];
        colcount = 0
        rowcount = 0
        result = ''

        downloadhour = ['000', '006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072',
                        '078', '084',
                        '090', '096', '102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162',
                        '168', '174',
                        '180', '186', '192', '198', '204', '210', '216', '222', '228', '234', '240']

        count = 0

        finalfilelist = []
        for count in range(0, len(downloadhour)):
            for file in files:
                #CNgfs.GFS2017121718.f120.png
                fcst = file[file.find('.') + file[file.find('.')+1:].find('.') + 3 : file.find('.png') ]
                #print(fcst)

                if fcst == downloadhour[count]:
                    finalfilelist.append(file)

        for file in finalfilelist:
            if file[-3:] == 'png':
                if colcount == 0:
                    result += '<div class="row mt">'

                result += '<div class="col-lg-4 col-md-4 col-sm-4 col-xs-12 desc"><div class="project-wrapper"><div class="project"><div class="photo-wrapper"><div class="photo">'
                result += '<a class="fancybox" href="static/images/model/GFS/WTP/'+file+'"><img class="img-responsive" src="static/images/model/GFS/WTP/'+file+'" alt=""></a>'
                result += '<div class="row mt"><div class="col-lg-12">'

                file = file[file.find('.')+1:]
                #year = file[file.find('GFS') + 3: file.find('GFS') + 7]
                month = file[file.find('GFS') + 7: file.find('GFS') + 9]
                day = file[file.find('GFS') + 9: file.find('GFS') + 11]
                hour = file[file.find('GFS') + 11: file.find('GFS') + 13]

                file = file[file.find('.') + 1:]
                fch = file[file.find('f') + 1: file.find('.')]

                result += '<p>地面要素（起报：' + month+'/'+day+'/'+hour + 'z  时效：' + fch +'）</p>'
                result += '</div></div></div><div class="overlay"></div></div></div></div></div><!-- col-lg-4 -->'

                if colcount == 2:
                    result += '</div><!-- /row -->'
                colcount += 1

        if iscookie()==True:
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            #print(open(r'product.html', 'r').read())
            return open(r'GFSsurfhead.html', 'r').read() + result + open(r'GFSsurfbottom.html', 'r').read()
        else:
            return web.redirect('login')

class GFS500:
    def GET(self):
        path = 'static/images/model/GFS/WGP'
        files = os.listdir(path)
        piclist = [];
        colcount = 0
        rowcount = 0
        result = ''

        downloadhour = ['000', '006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072',
                        '078', '084',
                        '090', '096', '102', '108', '114', '120', '126', '132', '138', '144', '150', '156', '162',
                        '168', '174',
                        '180', '186', '192', '198', '204', '210', '216', '222', '228', '234', '240']

        count = 0

        finalfilelist = []
        for count in range(0, len(downloadhour)):
            for file in files:
                #CNgfs.GFS2017121718.f120.png
                fcst = file[file.find('.') + file[file.find('.')+1:].find('.') + 3 : file.find('.png') ]
                #print(fcst)

                if fcst == downloadhour[count]:
                    finalfilelist.append(file)

        for file in finalfilelist:
            if file[-3:] == 'png':
                if colcount == 0:
                    result += '<div class="row mt">'

                result += '<div class="col-lg-4 col-md-4 col-sm-4 col-xs-12 desc"><div class="project-wrapper"><div class="project"><div class="photo-wrapper"><div class="photo">'
                result += '<a class="fancybox" href="static/images/model/GFS/WGP/'+file+'"><img class="img-responsive" src="static/images/model/GFS/WGP/'+file+'" alt=""></a>'
                result += '<div class="row mt"><div class="col-lg-12">'

                file = file[file.find('.')+1:]
                #year = file[file.find('GFS') + 3: file.find('GFS') + 7]
                month = file[file.find('GFS') + 7: file.find('GFS') + 9]
                day = file[file.find('GFS') + 9: file.find('GFS') + 11]
                hour = file[file.find('GFS') + 11: file.find('GFS') + 13]

                file = file[file.find('.') + 1:]
                fch = file[file.find('f') + 1: file.find('.')]

                result += '<p>高空要素（起报：' + month+'/'+day+'/'+hour + 'z  时效：' + fch +'）</p>'
                result += '</div></div></div><div class="overlay"></div></div></div></div></div><!-- col-lg-4 -->'

                if colcount == 2:
                    result += '</div><!-- /row -->'
                colcount += 1

        if iscookie()==True:
            i = web.input(access='True')
            web.setcookie('access', i.access, 600)
            #print(open(r'product.html', 'r').read())
            return open(r'GFS500head.html', 'r').read() + result + open(r'GFS500bottom.html', 'r').read()
        else:
            return web.redirect('login')

class success:
    def GET(self):
        if iscookie() == True:
            return open(r'success.html', 'r').read()
        else:
            return web.redirect('login')

class updatehistory:
    def GET(self):
        if iscookie() == True:
            return open(r'updatehistory.html', 'r').read()
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