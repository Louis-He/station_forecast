import web
urls = {
    '/index', 'index'
}
app = web.application(urls, globals())

class CookieSet:
    def GET(self):
        i = web.input(access='True')
        web.setcookie('access', i.age, 3600)
        return "Age set in your cookie"

class CookieGet:
    def GET(self):
        age=web.cookies().get('access')
        if age:
            return "Your age is: %s" % age
        else:
            return "Cookie does not exist."
if __name__ == "__main__":
    app.run()

