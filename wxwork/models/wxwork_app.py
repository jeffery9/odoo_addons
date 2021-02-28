# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import json
import logging
from datetime import timedelta

import requests
from odoo import api, models, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class wxworkApp(models.Model):
    _name = 'wxwork.app'
    _description = 'wxwork App'

    _rec_name = 'wxwork_app'
    _order = 'wxwork_app ASC'

    wxwork_app = fields.Char(string=u'App Name', required=True, copy=False)

    wxwork_agentid = fields.Char(string=u'Agent ID', required=True, copy=False)

    wxwork_secret = fields.Char(string=u'Secret', required=True, copy=False)

    company_id = fields.Many2one(
        string=u'Company',
        comodel_name='res.company',
        ondelete='restrict',
        default=False
    )

    access_token_ids = fields.One2many(
        string=u'Access Token',
        comodel_name='wxwork.access_token',
        inverse_name='app_id',
    )

    def get_access_token(self):
        for app in self:
            access_token = self.env['wxwork.access_token'].sudo().search(
                [('app_id', '=', app.id),
                 ('company_id', '=', app.company_id.id),
                 ('expire', '>', fields.Datetime.now())],
                limit=1
            )

            if access_token:
                return access_token.token
            # wxwork_access_token_url = self.env['ir.paramaters'].search([
            #     ('key', '=', 'wxwork_access_token_url')
            # ])

            # if not wxwork_access_token_url:
            #     raise UserError(
            #         'Found not wxwork_access_token_url in system paramaters')

            wxwork_access_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'

            payload = {
                'corpid': app.company_id.wxwork_corpid,
                'corpsecret': app.wxwork_secret
            }

            resp = requests.get(wxwork_access_token_url, params=payload)
            resp_timestamp = fields.Datetime.now()
            data = json.loads(resp.text)
            if data.get('errmsg') == 'ok':
                access_token = data.get('access_token')
                expires_in = data.get('expires_in')
                self.env['wxwork.access_token'].sudo().create({
                    'token': access_token,
                    'expire': resp_timestamp + timedelta(seconds=expires_in),
                    'app_id': app.id,
                    'company_id': app.company_id.id
                })
                return access_token

            else:
                raise UserError(
                    'some error occured \n \nerror code:  %s\nerror message:  \n  %s'
                    % (str(data.get('errcode')), data.get('errmsg'))
                )

    @api.model
    def call_back(self, data, company_id):
        _logger.info(data)

        return True


class wwxworkAccessToken(models.Model):
    _name = 'wxwork.access_token'
    _description = 'wxwork Access Token'

    _rec_name = 'token'
    _order = 'create_date DESC'

    token = fields.Char(string=u'Token', required=True, copy=False)

    expire = fields.Datetime(string=u'Expire', required=True)

    app_id = fields.Many2one(
        string=u'wxwork App',
        comodel_name='wxwork.app',
        ondelete='cascade',
        required=True
    )

    company_id = fields.Many2one(
        string=u'Company ID',
        comodel_name='res.company',
        ondelete='cascade',
        required=True
    )

    corpid = fields.Char(
        string=u'Corp Id',
        related='company_id.wxwork_corpid',
        readonly=True,
        store=True
    )
