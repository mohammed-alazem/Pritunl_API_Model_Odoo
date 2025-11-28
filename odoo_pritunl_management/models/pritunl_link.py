# -*- coding: utf-8 -*-
import sys
import os
from odoo import models, fields, api
from odoo.exceptions import UserError

lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class PritunlLink(models.Model):
    _name = 'pritunl.link'
    _description = 'Pritunl Link (Site-to-Site VPN)'
    _rec_name = 'name'

    name = fields.Char('Link Name', required=True)
    pritunl_id = fields.Char('Pritunl Link ID', readonly=True)
    config_id = fields.Many2one('pritunl.config', string='Configuration',
                                default=lambda self: self.env['pritunl.config'].get_default_config())
    status = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string='Status', default='offline')
    active = fields.Boolean('Active', default=True)
    synced = fields.Boolean('Synced', readonly=True)

    @api.model
    def action_sync_from_pritunl(self):
        """Sync links from Pritunl"""
        try:
            from links import list_links
            config = self.env['pritunl.config'].get_default_config()
            client = config.get_client()
            pritunl_links = list_links(client=client)

            for link_data in pritunl_links:
                existing = self.search([('pritunl_id', '=', link_data['id'])], limit=1)
                if existing:
                    existing.write({'name': link_data['name'], 'synced': True})
                else:
                    self.create({
                        'name': link_data['name'],
                        'pritunl_id': link_data['id'],
                        'config_id': config.id,
                        'synced': True
                    })
        except Exception as e:
            raise UserError(f"Failed to sync links: {str(e)}")
