# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # VPN User Relationship
    vpn_user_ids = fields.One2many('pritunl.user', 'partner_id', string='VPN Users')
    vpn_user_count = fields.Integer('VPN User Count', compute='_compute_vpn_user_count')
    has_vpn_access = fields.Boolean('Has VPN Access', compute='_compute_has_vpn_access', store=True)

    @api.depends('vpn_user_ids')
    def _compute_vpn_user_count(self):
        for partner in self:
            partner.vpn_user_count = len(partner.vpn_user_ids)

    @api.depends('vpn_user_ids', 'vpn_user_ids.disabled')
    def _compute_has_vpn_access(self):
        for partner in self:
            partner.has_vpn_access = any(not user.disabled for user in partner.vpn_user_ids)

    def action_create_vpn_user(self):
        """Create VPN user for this partner"""
        self.ensure_one()

        return {
            'name': 'Create VPN User',
            'type': 'ir.actions.act_window',
            'res_model': 'pritunl.user',
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.id,
                'default_name': self.name.lower().replace(' ', '.') if self.name else '',
                'default_email': self.email or '',
            },
            'target': 'new',
        }

    def action_view_vpn_users(self):
        """View VPN users for this partner"""
        self.ensure_one()

        return {
            'name': f'VPN Users - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'pritunl.user',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id}
        }
