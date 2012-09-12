# -*- coding: utf-8 -*-
import web
import config
#import db
#import re

t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', cache=config.cache, 
    globals=t_globals)

#render = web.template.render('templates/', cache=config.cache, 
#    globals={'sesion': web.ctx.session})

render._keywords['globals']['render'] = render

#renderbase_admin = web.template.render('templates/admin', base='layout')
#renderbase_admin = web.template.render('templates/admin', base='layout', cache=True)
renderbase_admin = web.template.render('templates/admin', 
        base='layout', cache=config.cache)
