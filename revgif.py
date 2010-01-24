import web
import os

render = web.template.render('templates/')
db = web.database(dbn='mysql', user='mateo', pw='b', db='revgifDB')

urls = (
    '/', 'index',
    '/add', 'add',
    '/(\d+)', 'show'
)

app = web.application(urls, globals())

filedir = './images/original/'
outdir = './images/reversed/'

class index:
    def GET(self):
        images = db.select('Image')
        return render.index(images)

class add:
    def POST(self):
        i = web.input(myfile={})
        gif = i['myfile'].file
        if gif != None:            
            self.add_gif(gif)

        raise web.seeother('/')

    def add_gif(self, gif):
        #TODO: validate that it's an animated gif

        n = db.insert('Image',OriginalFileName='')
        originalFN = str(n) + '.gif'
        outFN = originalFN
        fout = open(filedir + originalFN, 'w')
        fout.write(gif.read())
        fout.close()

        toRun = 'gimp -ib \'(reverse-gif "' + filedir + originalFN + '" "' + outdir + outFN + '")\' -b \'(gimp-quit 0)\''
        result = os.system(toRun)
        db.query("UPDATE Image SET OriginalFileName=$ofn, ReversedFileName=$rfn WHERE ID = $id", vars=dict(ofn=originalFN,rfn=outFN,id=n))

class show:
    def GET(self,id):
        res = db.select('Image', {'ID':id}, where="id = $ID")
        for item in res:
            web.header('Content-Type', 'image/gif')
            #web.debug("RFN: " + item.ReversedFileName)
            return open(outdir + item.ReversedFileName,'r').read()
        raise web.seeother('/')
        
        

if __name__ == "__main__": app.run()
