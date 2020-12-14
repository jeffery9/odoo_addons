# -*- coding: utf-8 -*-
{
    'name': "Sale Restrict Lot",

    'summary': """
        """,
    'description': """
    """,
    'author': "geninIT, 亘盈信息技术",
    'website': "http://www.geninit.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_stock'],

    # always loaded
    'data': [
        'views/views.xml',
    ],

    'installable': True,
    'auto_install': True,
}
