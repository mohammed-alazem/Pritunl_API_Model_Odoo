# -*- coding: utf-8 -*-
import sys
import os
from odoo import models, fields, api
from odoo.exceptions import UserError

lib_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


class PritunlOrganization(models.Model):
    _name = 'pritunl.organization'
    _description = 'Pritunl Organization'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char('Organization Name', required=True, tracking=True)
    pritunl_id = fields.Char('Pritunl ID', readonly=True, copy=False)
    config_id = fields.Many2one('pritunl.config', string='Configuration',
                                default=lambda self: self.env['pritunl.config'].get_default_config())

    # Relations
    user_ids = fields.One2many('pritunl.user', 'organization_id', string='Users')
    user_count = fields.Integer('User Count', compute='_compute_user_count', store=True)

    # Status
    active = fields.Boolean('Active', default=True)
    synced = fields.Boolean('Synced with Pritunl', readonly=True, copy=False)

    @api.depends('user_ids')
    def _compute_user_count(self):
        for record in self:
            record.user_count = len(record.user_ids)

    def _get_client(self):
        """Get Pritunl client from configuration"""
        if self.config_id:
            return self.config_id.get_client()
        return self.env['pritunl.config'].get_default_config().get_client()

    @api.model_create_multi
    def create(self, vals_list):
        """Create organization in Pritunl when created in Odoo"""
        records = super().create(vals_list)

        for record in records:
            if not record.pritunl_id:
                try:
                    from organizations import create_organization

                    client = record._get_client()
                    org = create_organization(name=record.name, client=client)

                    record.write({
                        'pritunl_id': org['id'],
                        'synced': True
                    })

                    record.message_post(
                        body=f"Organization created in Pritunl with ID: {org['id']}"
                    )
                except Exception as e:
                    raise UserError(f"Failed to create organization in Pritunl: {str(e)}")

        return records

    def write(self, vals):
        """Update organization in Pritunl when updated in Odoo"""
        result = super().write(vals)

        if 'name' in vals:
            for record in self.filtered(lambda r: r.pritunl_id):
                try:
                    from organizations import update_organization

                    client = record._get_client()
                    update_organization(
                        org_id=record.pritunl_id,
                        name=record.name,
                        client=client
                    )

                    record.message_post(
                        body=f"Organization updated in Pritunl: {record.name}"
                    )
                except Exception as e:
                    raise UserError(f"Failed to update organization in Pritunl: {str(e)}")

        return result

    def unlink(self):
        """Delete organization from Pritunl when deleted in Odoo"""
        for record in self:
            if record.pritunl_id:
                try:
                    from organizations import delete_organization

                    client = record._get_client()
                    delete_organization(org_id=record.pritunl_id, client=client)
                except Exception as e:
                    raise UserError(f"Failed to delete organization from Pritunl: {str(e)}")

        return super().unlink()

    @api.model
    def action_sync_from_pritunl(self):
        """Sync organizations from Pritunl to Odoo"""
        try:
            from organizations import list_organizations

            config = self.env['pritunl.config'].get_default_config()
            client = config.get_client()

            pritunl_orgs = list_organizations(client=client)

            for org_data in pritunl_orgs:
                existing = self.search([('pritunl_id', '=', org_data['id'])], limit=1)

                if existing:
                    existing.write({
                        'name': org_data['name'],
                        'synced': True
                    })
                else:
                    self.create({
                        'name': org_data['name'],
                        'pritunl_id': org_data['id'],
                        'config_id': config.id,
                        'synced': True
                    })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sync Successful',
                    'message': f'Synchronized {len(pritunl_orgs)} organizations from Pritunl',
                    'type': 'success',
                }
            }
        except Exception as e:
            raise UserError(f"Failed to sync organizations: {str(e)}")

    def action_view_users(self):
        """View users in this organization"""
        self.ensure_one()
        return {
            'name': f'Users in {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'pritunl.user',
            'view_mode': 'tree,form',
            'domain': [('organization_id', '=', self.id)],
            'context': {'default_organization_id': self.id}
        }
