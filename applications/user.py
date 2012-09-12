# -*- coding: utf-8 -*-
import web
from common import Sesion

from view import render

urls = (
  "", "reuser",
  "/", "monitoreo",
)


class reuser:
    def GET(self):
        raise web.seeother('/')

class monitoreo:
    @Sesion
    def GET(self):
        if web.ctx.session.get('logged_in'):
            print "Login: Si"
        else: print "Login: No"
        #raise web.seeother('/login')
        #return "\
        #        <p>Ruta actual en App user(%s) - Conectado: %s.</p> \
        #        <h1>Usted esta conectado.</h1><a href='/logout'>Desconectese</a>\
        #        <h1>Home.</h1><a href='/'>home</a>\
        #       " % (web.ctx.path, web.ctx.session.get('logged_in'))
        #return render.user.monitoreo(web.ctx.path, web.ctx.session.get('logged_in')) 
        return render.user.monitoreo(web.ctx.path, web.ctx.session) 

#class Login:
#    def GET(self):
#        web.ctx.session.logged_in = True
#        raise web.seeother('/')


app_user = web.application(urls, locals())
