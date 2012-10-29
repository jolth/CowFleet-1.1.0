# -*- coding: utf-8 -*-
import web

def Sesion(url):
    def verificaSesion(*args, **kwargs):
        if web.ctx.session.get('logged_in'):
            if web.ctx.homepath == web.ctx.session.homepath:
                return url(*args, **kwargs) 
        raise web.seeother(web.ctx.homedomain)
    return verificaSesion
