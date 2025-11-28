# -*- coding: utf-8 -*-
import sys
import os
from odoo import models, fields, api
from odoo.exceptions import UserError

lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class PritunlHost(models.Model):
    _name = 'pritunl.host'
    _description = 'Pritunl Host'
    _rec_name = 'name'

    name = fields.Char('Host Name', required=True)
    pritunl_id = fields.Char('Pritunl Host ID', readonly=True)
    config_id = fields.Many2one('pritunl.config', string='Configuration',
                                default=lambda self: self.env['pritunl.config'].get_default_config())
    public_address = fields.Char('Public Address')
    link_address = fields.Char('Link Address')
    status = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline')
    ], string='Status', default='offline')
    active = fields.Boolean('Active', default=True)
    synced = fields.Boolean('Synced', readonly=True)

    @api.model
    def action_sync_from_pritunl(self):
        """Sync hosts from Pritunl"""
        try:
            from hosts import list_hosts
            config = self.env['pritunl.config'].get_default_config()
            client = config.get_client()
            pritunl_hosts = list_hosts(client=client)

            for host_data in pritunl_hosts:
                existing = self.search([('pritunl_id', '=', host_data['id'])], limit=1)
                if existing:
                    existing.write({'name': host_data['name'], 'synced': True})
                else:
                    self.create({
                        'name': host_data['name'],
                        'pritunl_id': host_data['id'],
                        'config_id': config.id,
                        'synced': True
                    })
        except Exception as e:
            raise UserError(f"Failed to sync hosts: {str(e)}")
