# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    wxwork_corpid = fields.Char(string="wxwork Corp ID", )

    wxwork_app_ids = fields.One2many(
        string=u'wxwork App',
        comodel_name='wxwork.app',
        inverse_name='company_id',
    )

    wxwork_token = fields.Char(string=u'wxwork Token', )

    wxwork_aes_key = fields.Char(string=u'wxwork AES Key', )