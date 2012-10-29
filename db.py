# -*- coding: utf-8 -*-
import config
import sys

def listingUser(**k):
    """
        Determina si el usuario y contraseña coinciden. 
    """
    return config.DB.query("SELECT cliente_id AS clienteId, privilege_id FROM usuarios WHERE usuario=$i.username and passwd=$i.password", **k)

def listingPrivilege(**k):
    """
        Determina a que subaplicación se debe reenviar el usuario. 
    """
    result = config.DB.query("SELECT descrip FROM privileges WHERE id=$privilegeId", **k)
    return "".join(["/%s" % v for v in result[0].values()])

def getNameClient(**k):
    """
        Obtine el nombre del cliente
    """
    result = config.DB.query("SELECT nombre1, nombre2, apellido1, apellido2 FROM clientes WHERE id=$clienteId", **k)
    return result[0]

def getCompany(**k):
    """
        Obtiene la empresa según el cliente de la sesión.
    """
    result = config.DB.query("""
            SELECT c.id, c.name, c.document, m.descrip AS ciudad, c.direccion, c.email,
            c.sitio_web, ce.cargo_empresa AS cargo, sc.descrip AS t_companie,
            r.descrip AS regimen, td.descrip AS t_docu
            FROM companies c
            LEFT OUTER JOIN municipio AS m ON (c.ciudad=m.codigo)
            LEFT OUTER JOIN clientes_empresa AS ce ON (ce.empresa_id=c.id)
            LEFT OUTER JOIN sociedades_comerciales AS sc ON (sc.id=c.type_company_id)
            LEFT OUTER JOIN regimen AS r ON (r.id=c.regimen_id)
            LEFT OUTER JOIN type_document AS td ON (td.id=c.type_docu_id)
            WHERE ce.cliente_id=$clienteId""", **k)
    return result[0]

def listingDropdown(table, vars="id,name", order=None):
    """
        Obtiene una lista para los form.Dropdown().
    """
    result = config.DB.select(table, what=vars, order=order)
    return [tuple(i.values()) for i in result.list()]

def listingGPS():
    """
        Realiza un select de todos los GPS en las tablas public.gps y public.type_gps.
    """
    return config.DB.query("""SELECT g.id, g.name, g.fecha_creacion, t.descrip, 
            g.active FROM gps g INNER JOIN  type_gps t ON g.type = t.codigo;""")
    
def listUsuarios():
    """
        Realiza un select de todos los Usuarios.
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
    """
    from web.db import sqlquote
    result = config.DB.query("""SELECT p.phone, tp.name
            FROM phones_all pa, phones p, type_phone tp
            WHERE pa.phone_id=p.id AND tp.id=p.type AND pa.client_id=""" + sqlquote(id))
    return [tuple(i.values()) for i in result.list()]


def listingClients(id):
    """
        Lista los clientes propietarios de un vehiculo.
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
    """
    return config.DB.query("""SELECT l.position, v.placa, g.name, l.fecha, 
            l.velocidad, l.altura, l.satelites, l.ubicacion
            FROM vehiculos v, last_positions_gps l, gps g
            WHERE v.gps_id=g.id AND g.id=l.gps_id""")

def countEvent():
    """
        Retorna el numero de eventos sin gestionar.
    """
    return config.DB.query("""SELECT count(*) FROM eventos WHERE admin_state <> 't';""")


def insertPhone(storage, **sequence_id):
    """
    """
    from web.db import sqlquote

    for name in storage:
        if storage[name]:
            try:
                typePhone_id = (config.DB.select('type_phone', what="id", where="name=" + sqlquote(name)))[0].id
                seqPhone_id = config.DB.insert('phones', phone=storage[name], type=typePhone_id)
                seqPhone_all = config.DB.insert('phones_all', phone_id=seqPhone_id, **sequence_id)
            except:
                print "Error en insertPhone:"
                print sys.exc_info()
            
############### USER

def countEventClient(client_id):
    """
        Retorna el numero de eventos sin gestionar.
    """
    from web.db import sqlquote
    return config.DB.query("""SELECT count(*)
            FROM clientes_vehiculos cv, vehiculos v, gps g, eventos e
            WHERE cv.vehiculo_id=v.id AND v.gps_id=g.id AND g.id=e.gps_id 
            AND user_state <> 't' AND cv.cliente_id=""" + sqlquote(client_id))

def listingVehicleClient(client_id):
    """
       Retorna los vehiculos del cliente.
    """
    from web.db import sqlquote
    return config.DB.query("""SELECT v.id, lp.gps_id, v.placa, 
            lp.velocidad, lp.fecha, vs.motor, lp.ubicacion, lp.position
            FROM vehiculos v
            INNER JOIN clientes_vehiculos AS cv ON (cv.vehiculo_id = v.id)
            INNER JOIN last_positions_gps AS lp ON (lp.gps_id = v.gps_id)
            LEFT OUTER JOIN vehicle_state AS vs ON (vs.vehicle_id = v.id)
            WHERE cv.cliente_id=""" + sqlquote(client_id))

def eventsClient(client_id):
    """
        Retorna el numero de eventos sin gestionar.
    """
    from web.db import sqlquote
    return config.DB.query("""SELECT v.id AS vehi_id, v.placa, g.id AS gps_id, g.name, p.position, p.ubicacion, p.fecha,
            e.id AS event_id, p.id AS position_id, te.descrip
            FROM clientes_vehiculos cv, vehiculos v, gps g, eventos e, positions_gps p, type_event te
            WHERE cv.vehiculo_id=v.id AND v.gps_id=g.id AND g.id=e.gps_id
            AND p.id=e.positions_gps_id AND e.type=te.codigo
            AND user_state <> 't' AND cv.cliente_id=""" + sqlquote(client_id))

def reportday(vehiculo_id, fecha):
    """
        Genera un reporte de las posiciones de un vehiculo para un
        día detreminado.
    """
    from web.db import sqlquote
    start_date = fecha + ' 00:00:00' 
    end_date = fecha + ' 23:59:60' 
    return config.DB.query("""SELECT v.id, v.gps_id, v.placa, 
            p.velocidad, p.fecha, p.ubicacion, p.position
            FROM vehiculos v
            INNER JOIN positions_gps AS p ON (p.gps_id=v.gps_id)
            WHERE v.id=""" + sqlquote(vehiculo_id) + 
            """ and fecha between """ + sqlquote(start_date) + """ and """ + sqlquote(end_date))
         

