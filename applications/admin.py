# -*- coding: utf-8 -*-
"""
    Módulo Admin

    Autor: Jorge Toro [jolthgs@gmail.com]
"""
import sys
import web
from common import Sesion
from view import renderbase_admin
from config import DB
from view import render

urls = (
  "", "reuser",
  "/", "index",
  "/generalview", "generalview",
  "/viewmonitoreo", "viewmonitoreo",
  "/generalviewjson", "generalviewjson",
  "/addgps", "addgps",
  "/listgps", "listgps",
  "/editgps", "editgps",
  "/deletegps", "deletegps",
  "/addvehicle", "addvehicle",
  "/listvehicle","listvehicle",
  "/deletevehicle", "deletevehicle",
  "/assignclient", "assignclient",
  "/addclient", "addclient",
  "/listclient", "listclient",
  "/deleteclient", "deleteclient",
  "/adduser", "adduser",
  "/listuser","listuser",
  "/deleteuser","deleteuser",
  "/listgspjson", "listgspjson",
  "/listingphones", "listingphones",
  #"/events","events",
  "/listeventjson","listeventjson",
  "/viewmanagevent","viewmanagevent",
  "/managevents","managevents",
  "/listingclients","listingclients",
  "/deleteevent", "deleteevent",
  "/updateevent","updateevent",
)

class reuser:
    def GET(self):
        raise web.seeother('/')

class index:
    @Sesion
    def GET(self):
        return renderbase_admin.index(web.ctx.path, web.ctx.session) 

class addgps:
    @Sesion
    def GET(self):
        from appForm import formGps

        f = formGps() 
        return renderbase_admin.addgps(web.ctx.session, f) 

    def POST(self):
        from appForm import formGps

        f = formGps() 
        if f.validates():
            try:
                # Insert an entry into table 'gps'
                sequence_id = DB.insert('gps', **f.d)
            except: 
                return renderbase_admin.addgps(web.ctx.session, f, msgerr='El dispositivo %s ya existe' % f.d.name)
            return renderbase_admin.addgps(web.ctx.session, f, 'El dispositivo %s, se ha guardado con exito!' % f.d.name)
        else:
            return renderbase_admin.addgps(web.ctx.session, f, msgerr=u'Los datos no son válidos.')
            
class listgps:
    @Sesion
    def GET(self):
        from db import listingGPS
        return renderbase_admin.listgps(web.ctx.session, listingGPS())

class editgps:
    @Sesion
    def GET(self):
        i = web.input(id=None, name=None)
        return i.id, i.name 

class deletegps:
    @Sesion
    def GET(self):
        i = web.input(id=None, name=None)
        #print "deletegps", i.id, i.name
        try:
            DB.delete('gps', where="id=" + i.id)
        except:
            print "Error Inesperado /deletegps:", sys.exc_info()
        raise web.seeother('/listgps')
    
class addclient:
    @Sesion
    def GET(self):
        from appForm import formClient

        f = formClient() 
        return renderbase_admin.addclient(web.ctx.session, f) 

    def POST(self):
        from appForm import formClient

        f = formClient() 
        if f.validates():
            try:
                # Configure Storage Phones
                telefonos = {'fijo':f.d.fijo, 'celular':f.d.celular, 'pbx':f.d.pbx, 'fax':f.d.fax}
                try:
                    # The config to's name
                    nombres = f.d.nombres.split(' ') 
                    apellidos = f.d.apellidos.split(' ')
                    nombres.append('')
                    apellidos.append('')
                except:
                    print "Error Inesperado1 /addclient:", sys.exc_info()
                    return renderbase_admin.addclient(web.ctx.session, f, msgerr='Los Nombre o Apellidos no son validos.')

                # Insert an entry into table 'clientes'
                sequence_id = DB.insert('clientes', documento=f.d.documento, tipo_docu=f.d.tipo_docu, fecha_naci=f.d.fecha_naci, 
                        direccion=f.d.direccion.lower(), ciudad=f.d.ciudad, sexo_id=f.d.sexo_id, email=f.d.email.lower(), 
                        nombre1=nombres[0].lower(), nombre2=nombres[1].lower() or None, 
                        apellido1=apellidos[0].lower(), apellido2=apellidos[1].lower() or None)

                from db import insertPhone
                # Insert Phones
                insertPhone(telefonos, client_id=sequence_id)
                
            except: 
                print "Error Inesperado2 /addclient:", sys.exc_info()
                return renderbase_admin.addclient(web.ctx.session, f, msgerr='El Cliente: %s %s, ya existe' % (f.d.nombres, f.d.apellidos))
            return renderbase_admin.addclient(web.ctx.session, f, 'El Cliente: %s %s, se ha creado con exito!' % (f.d.nombres, f.d.apellidos))
        else:
            return renderbase_admin.addclient(web.ctx.session, f, msgerr=u'Los datos no son válidos.')

class listclient:
    @Sesion
    def GET(self):
        from db import listingAllClient
        return renderbase_admin.listclient(web.ctx.session, listingAllClient())

class deleteclient:
    @Sesion
    def GET(self):
        i = web.input(id=None)
        print "Deleteclient", i.id
        #return i.id
        try:
            DB.delete('clientes', where="id=" + i.id)
        except:
            print "Error Inesperado /deleteclient:", sys.exc_info()
        raise web.seeother('/listclient')
        
class adduser:
    @Sesion
    def GET(self):
        from appForm import formUser

        f = formUser() 
        return renderbase_admin.adduser(web.ctx.session, f) 

    def POST(self):
        from appForm import formUser

        f = formUser() 
        if f.validates():
            try:
                # Insert an entry into table 'usuarios'
                sequence_id = DB.insert('usuarios', usuario=f.d.usuario, passwd=f.d.passwd, 
                        privilege_id=f.d.privilege_id, activo=f.d.activo, cliente_id=f.d.cliente_id)
            except: 
                return renderbase_admin.adduser(web.ctx.session, f, msgerr='El usuario %s ya existe' % f.d.usuario)
            return renderbase_admin.adduser(web.ctx.session, f, 'El usuario %s, se ha creado con exito!' % f.d.usuario)
        else:
            return renderbase_admin.adduser(web.ctx.session, f, msgerr=u'Los datos no son válidos.')

class listuser:
    @Sesion
    def GET(self):
        from db import listUsuarios
        return renderbase_admin.listuser(web.ctx.session, listUsuarios())

class deleteuser:
    @Sesion
    def GET(self):
        i = web.input(id=None)
        print "deleteuser", i.id
        try:
            DB.delete('usuarios', where="id=" + i.id)
        except:
            print "Error Inesperado /deleteuser:", sys.exc_info()
        raise web.seeother('/listuser')

class addvehicle:
    @Sesion
    def GET(self):
        from appForm import formVeh

        f = formVeh() 
        #print f.render()
        return renderbase_admin.addvehicle(web.ctx.session, f) 
    
    def POST(self):
        from appForm import formVeh

        f = formVeh() 
        if f.validates():
            try:
                print "DATA:", f.d
                # Insert an entry into table 'vehiculos'
                sequence_id = DB.insert('vehiculos', 
                        placa=f.d.placa.lower(), modelo=f.d.modelo, marca_id=f.d.marca_id, gps_id=f.d.gps_id, 
                        cilindraje=f.d.cilindraje or None, carroceria_id=f.d.carroceria_id or None, 
                        ejes=f.d.ejes or None, clase_id=f.d.clase_id or None, 
                        servicio_id=f.d.servicio_id or None, combustible_id=f.d.combustible_id or None,
                        linea_id=f.d.linea_id or None, color_id=f.d.color_id or None)
            except: 
                return renderbase_admin.addvehicle(web.ctx.session, f, msgerr=u'El Vehículo %s ya existe' % f.d.placa)
            return renderbase_admin.addvehicle(web.ctx.session, f, u'El vehículo %s, se ha creado con exito!' % f.d.placa)
        else:
            return renderbase_admin.addvehicle(web.ctx.session, f, msgerr=u'Los datos no son válidos.')

class listvehicle:
    @Sesion
    def GET(self):
        from db import listingAllVehicle
        #return listvehicle
        return renderbase_admin.listvehicle(web.ctx.session, listingAllVehicle())

class assignclient:
    @Sesion
    def GET(self):
        return assignclient

class deletevehicle:
    @Sesion
    def GET(self):
        i = web.input(id=None, placa=None)
        #print "Delete Vehicle", i.id, i.placa
        #return i.id, i.placa
        try:
            DB.delete('vehiculos', where="id=" + i.id)
        except:
            print "Error Inesperado /deletevehicle:", sys.exc_info()
        raise web.seeother('/listvehicle')

class generalviewjson:
    @Sesion
    def GET(self):
        import simplejson as json 
        from db import generalView

        #views = DB.query("""SELECT l.position, v.placa, g.name, l.fecha, 
        #        l.velocidad, l.altura, l.satelites, l.ubicacion
        #        FROM vehiculos v, last_positions_gps l, gps g
        #        WHERE v.gps_id=g.id AND g.id=l.gps_id""")
        web.header('content-Type', 'application/json')
        def dthandler(obj):
            obj.fecha = obj.fecha.strftime("%F %H:%M:%S")
            return obj
        #return json.dumps([dthandler(row) for row in views])
        return json.dumps([dthandler(row) for row in generalView()])

class generalview:
    @Sesion
    def GET(self):
        return renderbase_admin.generalview(web.ctx.session)

class viewmonitoreo:
    @Sesion
    def GET(self): 
        from db import generalView
        return render.admin.viewmonitoreo(generalView())

class listgspjson:
    @Sesion
    def GET(self):
        import simplejson as json 
        from db import listingDropdown

        web.header('content-Type', 'application/json')
        return json.dumps(listingDropdown('gps', "id,name", "id DESC"))

class listingphones:
    @Sesion
    def GET(self):
        """
            http://127.0.0.1:8080/admin/listingphones?id=15

            [["7844983", "fijo"], ["3126783452", "celular"]]
        """
        import simplejson as json
        from db import listingPhones

        i = web.input(id=None)
        web.header('content-Type', 'application/json')
        return json.dumps(listingPhones(i.id))

#class events:
#    @Sesion
#    def GET(self):
#        return events

class listeventjson:
    @Sesion
    def GET(self):
        import simplejson as json 
        from db import countEvent
        web.header('content-Type', 'application/json')
        return json.dumps([row for row in countEvent()])

class viewmanagevent:
    @Sesion
    def GET(self): 
        from db import unmanagedEventListAdmin
        return render.admin.viewmanagevent(unmanagedEventListAdmin())

class managevents:
    @Sesion
    def GET(self):
        return renderbase_admin.managevents(web.ctx.session)

class listingclients:
    @Sesion
    def GET(self):
        """
            http://127.0.0.1:8080/admin/listingclients?id=5

            [["jorge,alonso,toro,hoyos", "11814584"]]
        """
        import simplejson as json
        from db import listingClients

        i = web.input(id=None)
        #print "ID VEHICLE:", i.id
        web.header('content-Type', 'application/json')
        return json.dumps(listingClients(i.id))
    
class deleteevent:
    @Sesion
    def GET(self):
        i = web.input(id=None)
        #print "********************************************** Delete Event:", i.id
        #return i.id
        try:
            DB.delete('eventos', where="id=$i.id", vars=locals())
        except:
            print "Error Inesperado /deleteclient:", sys.exc_info()
        raise web.seeother('/managevents')
    
class updateevent:
    @Sesion
    def GET(self):
        i = web.input(id=None)
        #print "****************************** Update Event:", i.id
        try:
            DB.update('eventos', where='id=$i.id', admin_state='t', vars=locals())
        except:
            print "Error Inesperado /updateevent:", sys.exc_info()    
        #return updateevent
        raise web.seeother('/managevents')



# App:
app_admin = web.application(urls, locals())
