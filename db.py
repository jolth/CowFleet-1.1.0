# -*- coding: utf-8 -*-
import config
import sys

#def listingUser(**k):
    #return config.DB.select('users', **k)
    #print **k
    #return config.DB.select('usuarios', **k)

def listingUser(**k):
    """
        Determina si el usuario y contraseña coinciden. 
    """
    #return config.DB.query("SELECT cliente_id AS clienteId, privilege_id FROM usuarios WHERE usuario=$name and pass=$passwd", **k)
    return config.DB.query("SELECT cliente_id AS clienteId, privilege_id FROM usuarios WHERE usuario=$i.username and passwd=$i.password", **k)


def listingPrivilege(**k):
    """
        Determina a que subaplicación se debe reenviar el usuario. 

        Usage:
        >>> from db import listingPrivilege
        >>> privilegeId=1
        >>> listingPrivilege(vars=locals())
            0.0 (1): SELECT descrip FROM privileges WHERE id=1
            u'/user'
        >>> 
    """
    #return config.DB.query("SELECT descrip FROM privileges WHERE id=$privilegeId", **k)
    result = config.DB.query("SELECT descrip FROM privileges WHERE id=$privilegeId", **k)
    return "".join(["/%s" % v for v in result[0].values()])


def getNameClient(**k):
    """
        Obtine el nombre del cliente

        usage:
            >>> from db import getNameClient
            >>> clienteId = 1
            >>> 
            >>> getNameClient(vars=locals())
             0.0 (1): SELECT nombre1, nombre2, apellido1, apellido2 FROM clientes WHERE id=1
             <Storage {'nombre2': u'alonso', 'apellido2': u'hoyos', 'apellido1': u'toro', 'nombre1': u'jorge'}>
            >>> r = getNameClient(vars=locals())
             0.0 (2): SELECT nombre1, nombre2, apellido1, apellido2 FROM clientes WHERE id=1
            >>> r.nombre1
             u'jorge'
            >>> 
    """
    result = config.DB.query("SELECT nombre1, nombre2, apellido1, apellido2 FROM clientes WHERE id=$clienteId", **k)
    #return "".join(["%s " % v for v in result[0].values()])
    #return result[0].values()
    return result[0]


#def listingDropdown(table, vars="id,name", order="id ASC"):
def listingDropdown(table, vars="id,name", order=None):
    """
        Obtiene una lista para los form.Dropdown().

        Usage:
        >>> from db import listingDropdown
        >>> r = listingDropdown('type_document')
            0.0 (4): SELECT id,name FROM type_document ORDER BY id ASC
        >>> r
        [(1, u'C\xe9dula de Ciudadan\xeda'), (2, u'N\xfamero de Identificaci\xf3n Tributaria'), 
        (3, u'Registro \xdanico Tributario'), (4, u'Tarjeta de Identidad'), (5, u'C\xe9dula de Extranjer\xeda')]
        >>> 
        >>> r = listingDropdown('type_gps', "codigo,descrip", "codigo ASC")
            0.0 (4): SELECT codigo,descrip FROM type_gps ORDER BY codigo ASC
        >>> r
        [(1, u'Antares'), (2, u'Skypatrol'), (3, u'HunterPro')]
        >>> 
    """
    #result = config.DB.select
    #result = config.DB.select('type_document', what="id,name")
    #result = config.DB.select('type_document', what="id,name", order="id DESC") # order="id ASC"
    # result = config.DB.select('type_document', what="id,name", order="id ASC")

    #result = config.DB.select(table, what=vars, order)
    result = config.DB.select(table, what=vars, order=order)
    return [tuple(i.values()) for i in result.list()]


def listingGPS():
    """
        Realiza un select de todos los GPS en las tablas public.gps y public.type_gps.

        Usage:
        >>> from db import listingGPS
        >>> a = listingGPS()
        >>> for i in a.list():
        ...     print i.name
        ... 
        GPS0001
        GPS0004
        ANT051
        ANT056
        ANT099
        >>>
    """
    return config.DB.query("""SELECT g.id, g.name, g.fecha_creacion, t.descrip, 
            g.active FROM gps g INNER JOIN  type_gps t ON g.type = t.codigo;""")
    
def listUsuarios():
    """
        Realiza un select de todos los Usuarios.

        Usage:
        >>> from db import listUsuarios
        >>> a = listUsuarios()
        >>>
        >>> for i in a.list():
            ...     print i
            ... 
            <Storage {'usuario': u'jorge', 'passwd': u'123456', \
            'fecha_caduca': datetime.datetime(2013, 8, 16, 19, 6, 12, 471588, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)),\ 
            'fecha_crea': datetime.datetime(2012, 8, 9, 19, 6, 12, 471588, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)), \
            'cliente': u'11814584', 'activo': True, 'descrip': u'user', 'id': 1}>
    """
    return config.DB.query("""
            SELECT u.id, u.usuario, u.passwd, p.descrip, c.documento AS cliente,
            u.fecha_crea, u.fecha_caduca, u.activo
            FROM usuarios u
            INNER JOIN  privileges p ON u.privilege_id=p.id
            INNER JOIN clientes c ON u.cliente_id=c.id;
            """)

def listingAllClient():
    """
        Query que abstrae todos los Clientes.
        Usage:
        >>> from db import listingAllClient
        >>> a = listingAllClient()
        >>> for i in a:
        ...     print i
        ... 
        <Storage {'nombre1': u'jorge', 'genero': u'Masculino', 'tipo': u'C\xe9dula de Ciudadan\xeda', 
        'nombre2': u'alonso', 'fecha_naci': datetime.date(1982, 11, 2), 
        'direccion': u'Cra 11 # 15-15 APT 601 BL 2B', 'apellido2': u'hoyos', 'apellido1': u'toro', 
        'id': 1, 'email': u'jolthgs@gmail.com', 'municipio': u'Manizales', 'documento': u'11814584'}>
    """
    return config.DB.query("""
            SELECT c.id, c.documento, td.descrip AS tipo,
            c.nombre1, c.nombre2, c.apellido1, c.apellido2,
            c.fecha_naci, s.descrip AS genero,
            c.direccion, m.descrip AS municipio, c.email
            FROM clientes AS c
            LEFT OUTER JOIN type_document AS td ON (c.tipo_docu=td.id)
            LEFT OUTER JOIN sexo AS s ON (c.sexo_id=s.id)
            LEFT OUTER JOIN municipio AS m ON (c.ciudad=m.codigo);
            """)

def listingPhones(id):
    """
        usage:
        >>> from db import listingPhones
        >>> a = listingPhones(15)
        0.01 (1): SELECT p.phone, tp.name
                    FROM phones_all pa, phones p, type_phone tp
                    WHERE pa.phone_id=p.id AND tp.id=p.type AND pa.client_id=15
        >>> for i in a:
        ...     print i
        ... 
        <Storage {'phone': u'7844983', 'name': u'fijo'}>
        <Storage {'phone': u'3126783452', 'name': u'celular'}>
        >>>
    """
    from web.db import sqlquote
    result = config.DB.query("""SELECT p.phone, tp.name
            FROM phones_all pa, phones p, type_phone tp
            WHERE pa.phone_id=p.id AND tp.id=p.type AND pa.client_id=""" + sqlquote(id))
    return [tuple(i.values()) for i in result.list()]


def listingClients(id):
    """
        Lista los clientes propietarios de un vehiculo.
        usage:
        >>> from db import listingClients
        >>> a = listingClients(5) # id del vehiculo 
        >>>
        >>> for i in a:
        ...     print i
        ... 
        (u'jorge,alonso,toro,hoyos', u'11814584')
        >>> 
    """
    from web.db import sqlquote

    result = config.DB.query("""
            SELECT (c.nombre1 || ',' || COALESCE(c.nombre2, '') || ',' || c.apellido1 || ',' || COALESCE(c.apellido2,'')) AS nombre,
            c.documento
            FROM clientes_vehiculos cv, clientes c
            WHERE cv.cliente_id=c.id AND cv.vehiculo_id=""" + sqlquote(id))
    return [tuple(i.values()) for i in result.list()]


def listingAllVehicle():
    """
        Query que abstrae todos los vehículos.

        Usage:
        >>> from db import listingAllVehicle
        >>> a = listingAllVehicle()
        >>> for i in a:
        ...     for k,v in i.items():
        ...             print "%s=%s" % (k,v),
        ... 
        servicio=None carroceria=Aspersora cilindraje=1.1 color=None 
        ejes=1 combustible=Etanol clase=Motocarro marca=Hino placa=ttq000 
        modelo=1964 linea=None name=ANT003 servicio=None carroceria=None 
        cilindraje=None color=None ejes=None combustible=None clase=None 
        marca=Renault placa=rjm270 modelo=2012 linea=None name=ANT049 
        servicio=None carroceria=None cilindraje=None color=None ejes=None 
        combustible=None clase=None marca=Jac placa=sta345 modelo=2008 
        linea=None name=ANT098
        >>> 
    """
    return config.DB.query("""
            SELECT v.id, v.placa, g.name, m.descrip AS marca, v.modelo,
            v.cilindraje, v.ejes, l.descrip AS linea,
            c.descrip AS clase, ca.descrip AS carroceria, co.descrip AS color,
            cb.descrip AS combustible, sv.descrip AS servicio
            FROM vehiculos AS v
            LEFT OUTER JOIN gps AS g ON (v.gps_id=g.id)
            LEFT OUTER JOIN marcas_vehiculo AS m ON (v.marca_id=m.id)
            LEFT OUTER JOIN liena_vehiculo AS l ON (v.linea_id=l.id)
            LEFT OUTER JOIN clase_vehiculo AS c ON (v.clase_id=c.id)
            LEFT OUTER JOIN carrocerias AS ca ON (v.carroceria_id=ca.id)
            LEFT OUTER JOIN colores AS co ON (v.color_id=co.id)
            LEFT OUTER JOIN combustibles AS cb ON (v.combustible_id=cb.id)
            LEFT OUTER JOIN servicio_vehiculo AS sv ON (v.servicio_id=sv.id);
            """)

def unmanagedEventListAdmin():
    """
        Query que obtiene todos los eventos no gestionados por el administrador.
        usage:
        >>> from db import unmanagedEventListAdmin
        >>> a = unmanagedEventListAdmin()
        >>> for i in a:
        ...     for k,v in i.items():
        ...             print "%s=%s" % (k,v),
        ... 
        vehicle_id=4 name=Panico id=46 user_state=False fecha=2012-08-28 11:56:54.638781-05:00 placa=ttq000 
        position_id=149 admin_state=False gps_name=ANT003 ubicacion=Carrera 6 # 16-2 a 16-100, Pereira, Risaralda, Colombia 
        gps_id=10 coord_state=False vehicle_id=4 name=Ignicion OFF id=45 user_state=False fecha=2012-08-28 11:56:51.360497-05:00 
        placa=ttq000 position_id=148 admin_state=False gps_name=ANT003 
        ubicacion=Carrera 6 # 16-2 a 16-100, Pereira, Risaralda, Colombia gps_id=10 coord_state=False
    """
    return config.DB.query("""
            SELECT e.id, te.name, e.fecha, e.type AS tipo_event,
            e.gps_id, g.name AS gps_name,
            v.placa, v.id AS vehicle_id,
            e.admin_state, e.user_state, e.coord_state,
            e.positions_gps_id AS position_id, p.ubicacion, p.position
            from eventos e
            LEFT OUTER JOIN type_event AS te ON e.type=te.codigo
            LEFT OUTER JOIN vehiculos AS v ON e.gps_id=v.gps_id
            LEFT OUTER JOIN gps AS g ON e.gps_id=g.id
            LEFT OUTER JOIN positions_gps AS p ON p.id=e.positions_gps_id
            WHERE e.admin_state='f' ORDER BY e.id DESC;
            """)


def generalView():
    """
        Usage:
        >>> from db import generalView
        >>> a = generalView()
        >>> a.list()
        [<Storage {'name': u'ANT003', 'velocidad': 1.0, \
        'fecha': datetime.datetime(2012, 8, 19, 7, 22, 34, 964809, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)), \
        'satelites': 3, 'placa': u'ttq000', 'ubicacion': u'Calle 20 # 6-1 a 6-99, Pereira, Risaralda, Colombia', 'position': '(4.81534,-75.69489)', 'altura': None}>,\
        <Storage {'name': u'ANT051', 'velocidad': 1.0, \
        'fecha': datetime.datetime(2012, 8, 19, 7, 21, 14, 64915, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None)),\
        'satelites': 3, 'placa': u'rjm270', 'ubicacion': u'Calle 20 # 6-1 a 6-99, Pereira, Risaralda, Colombia', 'position': '(4.81534,-75.69489)', 'altura': None}>]
        >>> a = generalView()
        >>> for i in a:
        ...     print i.placa
        ... 
        ttq000
        rjm270
        >>> 
    """
    return config.DB.query("""SELECT l.position, v.placa, g.name, l.fecha, 
            l.velocidad, l.altura, l.satelites, l.ubicacion
            FROM vehiculos v, last_positions_gps l, gps g
            WHERE v.gps_id=g.id AND g.id=l.gps_id""")

def countEvent():
    """
        Retorna el numero de eventos sin gestionar.
        Usage:
        >>> from db import countEvent
        >>> a = countEvent()

    """
    return config.DB.query("""SELECT count(*) FROM eventos WHERE admin_state <> 't';""")


def insertPhone(storage, **sequence_id):
    """
            >>> from db import insertPhone
            >>> telefonos = {'fijo':'44444444', 'celular':u'', 'pbx':u'', 'fax':u''}
            >>> insertPhone(telefonos, client_id=1) 
            0.0 (1): SELECT id FROM type_phone WHERE name='fijo'
            typePhone_id: 2
            0.0 (2): SELECT c.relname FROM pg_class c WHERE c.relkind = 'S'
            0.0 (3): INSERT INTO phones (phone, type) VALUES (44444444, 2); SELECT currval('phones_id_seq')
            seqPhone_id: 4
            0.0 (4): INSERT INTO phones_all (phone_id, client_id) VALUES (4L, 1)
            >>>
    """
    from web.db import sqlquote

    for name in storage:
        if storage[name]:
            try:
                typePhone_id = (config.DB.select('type_phone', what="id", where="name=" + sqlquote(name)))[0].id
                #print "typePhone_id:", typePhone_id
                # Insert public.phones
                seqPhone_id = config.DB.insert('phones', phone=storage[name], type=typePhone_id)
                #print "seqPhone_id:", seqPhone_id
                # Insert puiblic.phones_all
                seqPhone_all = config.DB.insert('phones_all', phone_id=seqPhone_id, **sequence_id)
                #print "seqPhone_all", seqPhone_all
            except:
                print "Error en insertPhone:"
                print sys.exc_info()
            

