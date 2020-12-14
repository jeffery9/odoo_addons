# -*- coding: utf-8 -*-
{
    'name':
        "wxWork",
    'summary':
        """
    weixin work base 

        """,
    'description':
        """

    weixin work base 

    weixin work push url  http[s]://web_url/wxwork/push

    """,
    'author':
        "geninit, Jeffery",
    'website':
        "http://www.geninit.cn",
    'category':
        'Utility',
    'version':
        '0.1',
    'depends': ['base'],
    "external_dependencies": {
        "python": ["Crypto"],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application':
        True
}
