# -*- coding:utf-8 -*-
"""
URL's
"""
import applications.user as user
import applications.admin as admin

urls = (
    "/user", user.app_user,
    "/admin", admin.app_admin,
    "/", 'Index',
    "/login", 'Login',
    "/logout", 'Logout'
)

