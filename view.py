# -*- coding: utf-8 -*-
import web
import config

t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', cache=config.cache, 
    globals=t_globals)

render._keywords['globals']['render'] = render

renderbase_admin = web.template.render('templates/admin', 
        base='layout', cache=config.cache)
