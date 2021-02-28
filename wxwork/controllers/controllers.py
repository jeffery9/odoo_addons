# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from .WXBizJsonMsgCrypt import WXBizJsonMsgCrypt


class wxwork(http.Controller):
    @http.route('/wxwork/push', auth='public', csrf=False)
    def push_event(self, **kw):
        http_request = request.httprequest
        data = http_request.data

        # validate url for wxwork callback services
        if http_request.method == 'GET' and 'msg_signature' in kw and 'timestamp' in kw and 'nonce' in kw and 'echostr' in kw:

            company_ids = request.env['res.company'].sudo().search([])
            reply_echostr = None
            for company_id in company_ids:
                if company_id.wxwork_token and company_id.wxwork_aes_key:
                    corpid = company_id.wxwork_corpid
                    token = company_id.wxwork_token
                    encoding_aes_key = company_id.wxwork_aes_key

                    wxwork_crypt = WXBizJsonMsgCrypt(
                        token, encoding_aes_key, corpid
                    )
                    result, reply_echostr = wxwork_crypt.VerifyURL(
                        kw['msg_signature'], kw['timestamp'], kw['nonce'],
                        kw['echostr']
                    )

                    if result == 0:
                        break

            return reply_echostr or ''

        elif http_request.method == 'POST' and 'msg_signature' in kw and 'timestamp' in kw and 'nonce' in kw:

            company_ids = request.env['res.company'].sudo().search([])
            for company_id in company_ids:
                if company_id.wxwork_token and company_id.wxwork_aes_key:
                    corpid = company_id.wxwork_corpid
                    token = company_id.wxwork_token
                    encoding_aes_key = company_id.wxwork_aes_key

                    wxwork_crypt = WXBizJsonMsgCrypt(
                        token, encoding_aes_key, corpid
                    )
                    result, plain_data = wxwork_crypt.DecryptMsg(
                        data, kw['msg_signature'], kw['timestamp'], kw['nonce']
                    )

                    if result == 0:
                        return request.env['wxwork.app'].call_back(
                            plain_data, company_id
                        )

            return ''

        else:
            return "Hello, world! :)"
