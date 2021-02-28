# -*- coding: utf-8 -*-
{
    'name':
        "Stock Quant History",
    'summary':
        """
    display quant history at specificed location
        """,
    'description':
        """
    """,
    'author':
        "geninIT, 亘盈信息技术",
    'website':
        "http://www.geninit.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':
        'Operations',
    'version':
        '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': ['views/views.xml', ],
    'installable':
        True,
    'auto_install':
        True
}
