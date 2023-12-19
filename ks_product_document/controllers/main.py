import base64
import json
import logging

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.documents.controllers.main import ShareRoute

logger = logging.getLogger(__name__)


class ShareRouteInherit(ShareRoute):
    @http.route('/documents/upload_attachment', type='http', methods=['POST'], auth="user")
    def upload_document(self, folder_id, ufile, tag_ids, document_id=False, partner_id=False, owner_id=False,
                        product_id=False):
        files = request.httprequest.files.getlist('ufile')
        result = {'success': _("All files uploaded")}
        tag_ids = tag_ids.split(',') if tag_ids else []
        if document_id:
            document = request.env['documents.document'].browse(int(document_id))
            ufile = files[0]
            try:
                data = base64.encodebytes(ufile.read())
                mimetype = ufile.content_type
                document.write({
                    'name': ufile.filename,
                    'datas': data,
                    'mimetype': mimetype,
                })
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)
                result = {'error': str(e)}
        else:
            vals_list = []
            for ufile in files:
                try:
                    mimetype = ufile.content_type
                    datas = base64.encodebytes(ufile.read())
                    vals = {
                        'name': ufile.filename,
                        'mimetype': mimetype,
                        'datas': datas,
                        'folder_id': int(folder_id),
                        'tag_ids': tag_ids,
                        'partner_id': int(partner_id),
                        'product_id': int(product_id)
                    }
                    if owner_id:
                        vals['owner_id'] = int(owner_id)
                    vals_list.append(vals)
                except Exception as e:
                    logger.exception("Fail to upload document %s" % ufile.filename)
                    result = {'error': str(e)}
            cids = request.httprequest.cookies.get('cids', str(request.env.user.company_id.id))
            allowed_company_ids = [int(cid) for cid in cids.split(',')]
            documents = request.env['documents.document'].with_context(allowed_company_ids=allowed_company_ids).create(
                vals_list)
            result['ids'] = documents.ids
        return json.dumps(result)
