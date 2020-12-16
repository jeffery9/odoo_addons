# -*- coding: utf-8 -*-
{
    'name': "wxwork Checkin",
    'summary': """
    weixin work Checkin 

        """,
    'description': """

    weixin work Checkin 


    """,
    'author': "geninit, Jeffery",
    'website': "http://www.geninit.cn",
    'category': 'Utility',
    'version': '0.1',
    'depends': ['wxwork','hr', 'hr_attendance'],
    "external_dependencies": {
        "python": ["Crypto"],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True
}
