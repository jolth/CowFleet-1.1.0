# -*- coding:utf-8 -*-
"""
URL's
"""
import applications.user as user
import applications.admin as admin
import applications.coordinator as coordinator

#urls = (
#    '/(styles|js|img)/(.*)', 'static',
#    '/', 'login'
#)

urls = (
    "/user", user.app_user,
    "/admin", admin.app_admin,
    "/coordinator", coordinator.app_coordinator,
    # 
    "/", 'Index',
    "/login", 'Login',
    "/logout", 'Logout'
)



