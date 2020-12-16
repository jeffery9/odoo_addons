# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import request
from .WXBizJsonMsgCrypt import WXBizJsonMsgCrypt


class wxwork(http.Controller):
    @http.route('/wxwork/push', auth='public')
    def index(self, **kw):
        # validate url for wxwork callback services
        if 'msg_signature' in kw and 'timestamp' in kw and 'nonce' in kw and 'echostr' in kw:

            company_ids = request.env.companies
            reply_echostr = None
            for company_id in company_ids:
                if company_id.wxwork_token and company_id.wxwork_aes_key:
                    corpid = company_id.wxwork_corpid
                    token = company_id.wxwork_token
                    encoding_aes_key = company_id.wxwork_aes_key

                    wxwork_crypt = WXBizJsonMsgCrypt(token, encoding_aes_key,
                                                     corpid)
                    result, reply_echostr = wxwork_crypt.VerifyURL(
                        kw['msg_signature'], kw['timestamp'], kw['nonce'],
                        kw['echostr'])

                    if result == 0:
                        break

            if reply_echostr:
                return reply_echostr

        else:
            return request.env['wxwork.app'].call_back(kw)

        return "Hello, world"
