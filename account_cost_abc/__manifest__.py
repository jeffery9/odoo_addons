# -*- coding: utf-8 -*-
{
    'name': "Activity Based Costing",
    'summary': """
        """,
    'description': """
    """,
    'author': "geninIT, 亘盈信息技术",
    'website': "http://www.geninit.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/cost_pool.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['demo/demo.xml', ],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
