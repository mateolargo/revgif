import web

render = web.template.render('templates/')
db = web.database(dbn='mysql', user='mateo', pw='b', db='revgifDB')

urls = (
    '/', 'index',
    '/add', 'add'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        images = db.select('Image')
        return render.index(images)

class add:
    def POST(self):
        i = web.input(myfile={})
        filedir = './images/original'
        gif = i['myfile'].file
        if gif != None:
            fout = open(filedir + '/' + 'test.gif', 'w')
            fout.write(gif.read())
            fout.close()

        #n = db.insert('Image', FileName=i.filename)
        raise web.seeother('/')

if __name__ == "__main__": app.run()
