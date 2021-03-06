# -*- coding: utf-8 -*-
"""
    Autor: Jorge A. Toro [jolthgs@gmail.com]
"""
import sys, os
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(ROOT_PATH)
import web
from urls import urls
import view, config
from view import render

app = web.application(urls, locals())

if web.config.get('_sesion') is None:
    session = web.session.Session(app, web.session.DiskStore('sesiones'), {'count': 0})
    web.config._sesion = session
else:
    session = web.config._sesion
            
def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))

class Index:
    def GET(self):
        if session.get('logged_in', False):
            referer = web.ctx.env.get('HTTP_REFERER', web.ctx.homedomain)
            if referer is web.ctx.homedomain: raise  web.seeother('/login') 
            raise web.seeother(referer)
        raise  web.seeother('/login')

class Login:
    def GET(self):
        return render.login()

    def POST(self):
        from db import listingUser

        i = web.input()

        result = listingUser(vars=locals())
        if result:
            from db import listingPrivilege, getNameClient

            clienteId, privilegeId = result[0].values()
            session.logged_in = True
            session.user = i.username
            # App Companies:
            #if privilegeId == 4:
            #    try:
            #        from db import getCompany
            #        session.company = getCompany(vars=locals())
            #    except:
                    # Si el cliente no esta asociado a una empresa en public.clientes_empresa:
            #        session.logged_in = False
            #        return render.login(u'Sesión %s. No se tiene una empresa parar este usuario.' % session.get('logged_in', False))
                    

            # ID Cliente (clientes.id):
            session.clienteId = clienteId
            # Nombre del cliente:
            session.username = getNameClient(vars=locals())
            # Homepath según usuarios.privilege_id
            session.homepath = listingPrivilege(vars=locals())
            raise web.seeother(session.homepath)
        else:
            return render.login(u'Sesión %s. Usuario o Contraseña inválido(s).' % session.get('logged_in', False))

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')


if __name__ == "__main__":
    app.run()
