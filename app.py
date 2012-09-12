# -*- coding: utf-8 -*-
"""
    Autor: Jorge A. Toro [jolthgs@gmail.com]
"""
# Interfaz
import sys, os
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(ROOT_PATH)

# Módulos
import web
from urls import urls
import view, config
from view import render


#web.config.debug = False # descomentar en producción
app = web.application(urls, locals())
#session = web.session.Session(app, web.session.DiskStore('sesiones'), {'count': 0}) # descomentar en producción

# Quitar en Producción:
if web.config.get('_sesion') is None:
    session = web.session.Session(app, web.session.DiskStore('sesiones'), {'count': 0})
    web.config._sesion = session
else:
    session = web.config._sesion
            

def session_hook():
    web.ctx.session = session
    #web.template.Template.globals['session'] = session
    #web.template.Template.globals['session'] = web.ctx.session
    #print "\nGLOBAL:", dir(web.template.Template.globals.values())
    #web.template.render(globals={'sesion':session})
    print "\nGLOBAL:", dir(web.template.Template.globals)
    print "\nGLOBAL VALUES:", dir(web.template.Template.globals.values())
    #print "RENDER", dir(render._add_global)
    print "\nSESSION", dir(web.ctx.session)

app.add_processor(web.loadhook(session_hook))


class Index:
    def GET(self):
        if session.get('logged_in', False):
            #raise web.seeother('/user')
            #raise web.seeother(web.ctx.env.get('HTTP_REFERER', web.ctx.homedomain))
            #homedomain = web.ctx.homedomain
            #print "HOMEDOMAIN:", homedomain
            referer = web.ctx.env.get('HTTP_REFERER', web.ctx.homedomain)
            #referer = web.ctx.env.get('HTTP_REFERER', 'http://127.0.0.1:8080')
            #referer = web.ctx.env.get('HTTP_REFERER', '/user')
            #referer = web.ctx.env.get('HTTP_REFERER', 'http://gmys.com.co')
            print "REFERER:", referer
            print "HOMEDOMAIN:", web.ctx.homedomain
            if referer is web.ctx.homedomain: raise  web.seeother('/login') # Resuelve el derefer
            raise web.seeother(referer)
        #return '<h1>Usted no esta conectado.</h1><a href="/login">Conectese Ahora</a>'
        raise  web.seeother('/login')

class Login:
    def GET(self):
        #l = login()
        #return template.login(login)
        #return render.login(login)
        return render.login()

    def POST(self):
        from db import listingUser
        #l = login()

        # Validamos los campos del formulario
        #if not l.validates():
            #return template.login(login, 'Debe rellenar los campos')
        #    return render.login(login, 'Debe rellenar los campos')
        #else:
        i = web.input()
        #name, passwd = web.input().name, web.input().passwd
        #name, passwd = web.input().name, web.input().passwd

        #try:
            # Conexión a SQLite 
            #conn = db.connect("users.db")
            #cur = conn.cursor()
            # Realizamos el Query. 
            #check = cur.execute('select * from users where username=? and password=?', (i.Username, i.Password))
        
            # check.fetchone() sera una tupla (u'jolth', u'123456') o None sino existe. 
            #if check.fetchone():
        #if listingUser('usuario=$i.username and pass=$i.password', vars=locals()):
        
        result = listingUser(vars=locals())
        if result:
            from db import listingPrivilege, getNameClient

            clienteId, privilegeId = result[0].values()
            print "clienteId:", clienteId
            print "privilegeId:", privilegeId
            session.logged_in = True
            #session.username = i.username

            # ID Cliente (clientes.id):
            session.clienteId = clienteId
            # Nombre del cliente:
            session.username = getNameClient(vars=locals())

            print "Primer NOMBRE DEL Cliente:", session.username.nombre1
            # Seeother Según user.privilege
            #raise web.seeother('/user')

            # Homepath según usuarios.privilege_id
            session.homepath = listingPrivilege(vars=locals())
            #raise web.seeother(listingPrivilege(vars=locals()))
            print "HOMEPPPPPPP:", session.homepath
            raise web.seeother(session.homepath)
            #raise web.seeother('/')
        else:
            #return template.login(login, 'Usuario y Contraseña invalidos. session %s' % session.get('logged_in', False))
            return render.login('Sesión %s: Usuario/Contraseña invalidos.' % session.get('logged_in', False))
        #except: # db.Error, e:
        #    print >> sys.stderr, '-'*60
        #    print >> sys.stderr.write("Error: %s\n" % e.args[0])
        #    print >> sys.stderr, '-'*60
        #finally:
        #    cur.close()
        #    conn.close()
             

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')


if __name__ == "__main__":
    app.run()
