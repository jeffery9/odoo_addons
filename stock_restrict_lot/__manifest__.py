# -*- coding: utf-8 -*-
{
    'name': "Stock Restrict Lot",

    'summary': """
        """,
    'description': """
    """,
    'author': "geninIT, 亘盈信息技术",
    'website': "http://www.geninit.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    
    'installable': True,

}
