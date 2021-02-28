# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    wxwork_corpid = fields.Char(string="wxwork Corp ID", )

    wxwork_token = fields.Char(string=u'wxwork Token', )

    wxwork_aes_key = fields.Char(string=u'wxwork AES Key', )

    wxwork_app_ids = fields.One2many(
        string=u'wxwork App',
        comodel_name='wxwork.app',
        inverse_name='company_id',
    )

    @api.constrains('wxwork_corpid')
    def _check_wxwork_corpid(self):
        for record in self:
            if record.wxwork_corpid and self.search(
                [('wxwork_corpid', '=', record.wxwork_corpid)]) > 1:
                raise UserError(
                    _(u'duplicated corpid %s found!') % (record.wxwork_corpid)
                )
