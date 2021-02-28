# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    wxwork_userid = fields.Char(string=u'wxwork User ID', )

    wxwork_checkin_ids = fields.One2many(
        string=u'wxwork Checkin',
        comodel_name='wxwork.checkin',
        inverse_name='employee_id',
    )
